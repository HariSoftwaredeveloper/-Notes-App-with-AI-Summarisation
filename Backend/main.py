# backend/main.py
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Import modules using relative paths
try:
    # When running as package: `uvicorn Backend.main:app`
    from . import models, auth, ai_service
    from .models import UserDB, NoteDB, Note, NoteCreate, UserCreate
    from .database import get_db, engine
except Exception:
    # When running as module from `Backend` dir: `uvicorn main:app`
    import models, auth, ai_service
    from models import UserDB, NoteDB, Note, NoteCreate, UserCreate
    from database import get_db, engine

# Initialize FastAPI and create database tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# --- Auth Endpoints ---

# Use explicit dependency injection for get_db
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
CURRENT_USER_DEPENDENCY = Annotated[UserDB, Depends(auth.get_current_user)]

@app.post("/signup", response_model=models.Token)
def signup_user(user: UserCreate, db: DB_DEPENDENCY):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = UserDB(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = auth.create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=models.Token)
def login_for_access_token(user_in: UserCreate, db: DB_DEPENDENCY):
    user = db.query(UserDB).filter(UserDB.email == user_in.email).first()
    if not user or not auth.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Note CRUD Endpoints ---
@app.get("/notes", response_model=List[Note])
def read_notes(db: DB_DEPENDENCY, current_user: CURRENT_USER_DEPENDENCY):
    return db.query(NoteDB).filter(NoteDB.owner_id == current_user.id).order_by(NoteDB.updated_at.desc()).all()

@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: DB_DEPENDENCY, current_user: CURRENT_USER_DEPENDENCY):
    db_note = NoteDB(**note.model_dump(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note_in: NoteCreate, db: DB_DEPENDENCY, current_user: CURRENT_USER_DEPENDENCY):
    db_note = db.query(NoteDB).filter(NoteDB.id == note_id, NoteDB.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db_note.title = note_in.title
    db_note.content = note_in.content
    db_note.summary = None # Clear summary on content change
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: DB_DEPENDENCY, current_user: CURRENT_USER_DEPENDENCY):
    db_note = db.query(NoteDB).filter(NoteDB.id == note_id, NoteDB.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return

# --- AI Summarization Endpoint ---
@app.post("/notes/{note_id}/summarize", response_model=Note)
def summarize_note(note_id: int, db: DB_DEPENDENCY, current_user: CURRENT_USER_DEPENDENCY):
    db_note = db.query(NoteDB).filter(NoteDB.id == note_id, NoteDB.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
        
    summary = ai_service.summarize_text(db_note.content)
    
    db_note.summary = summary
    db.commit()
    db.refresh(db_note)
    return db_note
