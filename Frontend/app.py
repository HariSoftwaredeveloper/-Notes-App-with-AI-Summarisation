# frontend/app.py
import streamlit as st
import requests
import json
from datetime import datetime

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000" # Must match the running FastAPI port

# --- State Initialization ---
def init_session_state():
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    if 'notes' not in st.session_state:
        st.session_state['notes'] = []
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'list'
    if 'edit_note' not in st.session_state:
        st.session_state['edit_note'] = None

# --- API Helper Functions ---
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}", "Content-Type": "application/json"}
    return {"Content-Type": "application/json"}

def fetch_notes():
    if not st.session_state.is_logged_in:
        st.session_state.notes = []
        return
    try:
        response = requests.get(f"{API_BASE_URL}/notes", headers=get_headers())
        if response.status_code == 200:
            st.session_state.notes = response.json()
        elif response.status_code == 401:
            st.warning("Session expired. Please log in again.")
            st.session_state.is_logged_in = False
            st.session_state.token = None
            st.rerun()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Ensure FastAPI is running.")

# --- Action Callbacks ---
def switch_to_editor(note=None):
    st.session_state.edit_note = note
    st.session_state.current_view = 'editor'
    st.rerun()

def summarize_action(note_id):
    """Callback function to call the AI summarization endpoint."""
    with st.spinner("🧠 Azure AI is generating summary..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/notes/{note_id}/summarize",
                headers=get_headers()
            )
            if response.status_code == 200:
                st.toast("Summary generated!", icon="✅")
                fetch_notes() 
            else:
                st.error(f"Summarization failed: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI backend.")
            
def delete_action(note_id):
    """Callback function to delete a note."""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/notes/{note_id}",
            headers=get_headers()
        )
        if response.status_code == 204:
            st.success("Note deleted.")
            fetch_notes()
            st.rerun()
        else:
            st.error(f"Failed to delete note: {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI backend.")

# --- Frontend Component Renderers ---
def render_auth():
    st.sidebar.title("🔐 User Access")
    
    if st.session_state.is_logged_in:
        st.sidebar.success("Logged In!")
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.clear()
            st.rerun()
        return True
    
    auth_mode = st.sidebar.radio("Mode", ("Login", "Signup"), key="auth_mode_radio")
    
    with st.sidebar.form(key=f'{auth_mode}_form'):
        email = st.text_input("Email", key=f"{auth_mode}_email")
        password = st.text_input("Password", type="password", key=f"{auth_mode}_password")
        submit_button = st.form_submit_button(auth_mode)
        
        if submit_button:
            endpoint = "/token" if auth_mode == "Login" else "/signup"
            try:
                response = requests.post(
                    f"{API_BASE_URL}{endpoint}",
                    json={"email": email, "password": password}
                )
                
                if response.status_code in (200, 201):
                    token_data = response.json()
                    st.session_state.token = token_data['access_token']
                    st.session_state.is_logged_in = True
                    st.success(f"{auth_mode} successful! Reloading notes...")
                    fetch_notes()
                    st.rerun()
                else:
                    st.error(f"{auth_mode} failed: {response.json().get('detail', 'Invalid credentials or email taken')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Ensure it is running at http://127.0.0.1:8000.")
                
    return False

def render_note_editor():
    is_editing = st.session_state.edit_note is not None
    note_data = st.session_state.edit_note if is_editing else {"title": "", "content": "", "id": None}
    
    st.header("✏️ " + ("Edit Note" if is_editing else "Create New Note"))
    
    with st.form(key="note_editor_form", clear_on_submit=False):
        new_title = st.text_input("Title", value=note_data['title'])
        new_content = st.text_area("Content", value=note_data['content'], height=300)
        
        col1, col2 = st.columns(2)
        with col1:
            save_button = st.form_submit_button("💾 Save Note" if is_editing else "➕ Add Note")
        with col2:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.current_view = 'list'
                st.session_state.edit_note = None
                st.rerun()
        
        if save_button:
            data = {"title": new_title, "content": new_content}
            
            if len(new_title) == 0 or len(new_content) == 0:
                st.warning("Title and Content cannot be empty.")
            else:
                if is_editing:
                    response = requests.put(
                        f"{API_BASE_URL}/notes/{note_data['id']}", 
                        json=data, 
                        headers=get_headers()
                    )
                else:
                    response = requests.post(
                        f"{API_BASE_URL}/notes", 
                        json=data, 
                        headers=get_headers()
                    )
                
                if response.status_code in (200, 201):
                    st.success("Note saved successfully! (Summary cleared if content changed)")
                    st.session_state.current_view = 'list'
                    st.session_state.edit_note = None
                    fetch_notes()
                    st.rerun()
                else:
                    st.error(f"Failed to save note. Error: {response.json().get('detail', 'API error')}")

def render_note_card(note):
    """Renders a single note preview with actions."""
    with st.expander(f"📄 **{note['title']}** (Updated: {note['updated_at'].split('T')[0]})", expanded=False):
        
        if note['summary']:
            st.caption("--- **AI Summary** (from Azure OpenAI) ---")
            st.info(note['summary'])
            st.caption("--- Full Content ---")
        
        st.markdown(note['content'])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("✍️ Edit", key=f"edit_{note['id']}", on_click=switch_to_editor, args=(note,))
        with col2:
            btn_text = "🔄 Resummarize" if note['summary'] else "🧠 Summarize with AI"
            st.button(btn_text, key=f"sum_{note['id']}", on_click=summarize_action, args=(note['id'],))
        with col3:
            st.button("🗑️ Delete", key=f"del_{note['id']}", on_click=delete_action, args=(note['id'],))
        
def render_note_list():
    st.header("🗃️ Your Notes")
    if st.button("➕ Create New Note", key="new_note_btn"):
        switch_to_editor(note=None)
    
    st.markdown("---")
    
    if st.session_state.notes:
        for note in st.session_state.notes:
            render_note_card(note)
    else:
        st.info("You don't have any notes yet. Click 'Create New Note' to start!")

# --- Main Streamlit App Logic ---
def main_app():
    init_session_state()

    st.set_page_config(layout="wide", page_title="AI Notes App")
    st.title("Azure AI-Powered Notes ☁️")

    is_authenticated = render_auth()

    if is_authenticated:
        if st.session_state.current_view == 'list':
            fetch_notes()
            render_note_list()
        elif st.session_state.current_view == 'editor':
            render_note_editor()
    else:
        st.image("https://images.unsplash.com/photo-1517849845537-4d257902454a?fit=crop&w=1400&h=800")
        st.markdown("### Secure, Pythonic Notes Application")
        st.markdown("* Backend: **FastAPI** (Authentication, CRUD, API Services)")
        st.markdown("* Frontend: **Streamlit** (Simple, Interactive UI)")
        st.markdown("* AI: **Azure OpenAI Service (GPT-4o)** for automatic summarization")

if __name__ == '__main__':
    main_app()
