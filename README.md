📝 Azure AI Notes App

An end-to-end full-stack application for note-taking featuring secure user authentication (FastAPI, JWT) and intelligent summarization powered by Azure OpenAI Service.

✨ Key Features

    Secure Authentication: User signup and login secured using FastAPI and JSON Web Tokens (JWT).

    Notes Management: Full CRUD (Create, Read, Update, Delete) functionality for managing personal notes.

    AI Summarization: Utilizes Azure OpenAI Service (GPT-4o) to generate concise, 1-3 sentence summaries of long notes with a dedicated API endpoint.

    Modern Stack: Frontend built with Streamlit for rapid development and an interactive UI; Backend built with high-performance FastAPI and SQLAlchemy (SQLite).

🚀 Getting Started

Follow these steps to set up and run the application locally.

1. Prerequisites

You must have Python 3.9+ and pip installed.

2. Project Setup
1.Clone the Repository:

git clone [YOUR_REPOSITORY_URL]
cd [YOUR_REPOSITORY_NAME]
2.Create a Virtual Environment (Recommended):
Bash

python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux   

3.Install Dependencies:
Bash

pip install -r requirements.txt

3.Configuration (.env File)

Create a file named .env in the root directory of the project (/notes_app) and populate it with your API keys and a secret key for authentication.
Code snippet

# --- Azure OpenAI Credentials ---
AZURE_OPENAI_API_KEY="7dA5uVLtdvRfQfnxI9M6qV1dFayX0QtLeNmL5QdK6QV4PduYPMBnZQQJ99ALAC5T7U2XJ3w3AAABACOGflMc"
AZURE_OPENAI_ENDPOINT="https://francecentral.api.cognitive.microsoft.com/"
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o" # Must match your deployment name

# --- Authentication Secret ---
SECRET_KEY="YOUR_SUPER_SECURE_JWT_KEY_GENERATE_A_LONG_RANDOM_STRING"

4.Running the Application (Two Terminals Required)

The backend and frontend must run simultaneously.

A. Start the FastAPI Backend

The backend must be run from the root directory to resolve module imports correctly.
Bash

# Ensure you are in the project root: /notes_app
cd backend
uvicorn main:app --reload

The FastAPI service will start at: http://127.0.0.1:8000

B. Start the Streamlit Frontend

Open a second terminal and run the Streamlit application.
Bash

# Ensure you are in the project root: /notes_app
cd frontend
streamlit run app.py

The Streamlit UI will open automatically in your browser, typically at: http://localhost:8501

👨‍💻 Usage Instructions

    Authentication: Use the sidebar on the Streamlit app to Signup (creates a user in the local database) and then Login with your credentials.

    Note Creation: Click the "➕ Create New Note" button to enter the editor view.

    Summarization: Once a note is saved, click the "🧠 Summarize with AI" button on the note card. The FastAPI backend will send the content to the Azure OpenAI service, retrieve the summary, and update the note in the database.
That's a great final step! A well-written README.md is essential for any GitHub project, as it acts as the primary documentation and entry point for users and potential contributors.

Here is a complete, professional, and detailed README file tailored specifically for your Azure AI Notes App, including setup instructions for both the FastAPI backend and the Streamlit frontend.

📝 Azure AI Notes App

An end-to-end full-stack application for note-taking featuring secure user authentication (FastAPI, JWT) and intelligent summarization powered by Azure OpenAI Service.

✨ Key Features

    Secure Authentication: User signup and login secured using FastAPI and JSON Web Tokens (JWT).

    Notes Management: Full CRUD (Create, Read, Update, Delete) functionality for managing personal notes.

    AI Summarization: Utilizes Azure OpenAI Service (GPT-4o) to generate concise, 1-3 sentence summaries of long notes with a dedicated API endpoint.

    Modern Stack: Frontend built with Streamlit for rapid development and an interactive UI; Backend built with high-performance FastAPI and SQLAlchemy (SQLite).

🚀 Getting Started

Follow these steps to set up and run the application locally.

1. Prerequisites

You must have Python 3.9+ and pip installed.

2. Project Setup

    Clone the Repository:
    Bash

git clone [YOUR_REPOSITORY_URL]
cd [YOUR_REPOSITORY_NAME]

Create a Virtual Environment (Recommended):
Bash

python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

Install Dependencies:
Bash

    pip install -r requirements.txt

3. Configuration (.env File)

Create a file named .env in the root directory of the project (/notes_app) and populate it with your API keys and a secret key for authentication.
Code snippet

# --- Azure OpenAI Credentials ---
AZURE_OPENAI_API_KEY="7dA5uVLtdvRfQfnxI9M6qV1dFayX0QtLeNmL5QdK6QV4PduYPMBnZQQJ99ALAC5T7U2XJ3w3AAABACOGflMc"
AZURE_OPENAI_ENDPOINT="https://francecentral.api.cognitive.microsoft.com/"
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o" # Must match your deployment name

# --- Authentication Secret ---
SECRET_KEY="YOUR_SUPER_SECURE_JWT_KEY_GENERATE_A_LONG_RANDOM_STRING"

4. Running the Application (Two Terminals Required)

The backend and frontend must run simultaneously.

A. Start the FastAPI Backend

The backend must be run from the root directory to resolve module imports correctly.
Bash

# Ensure you are in the project root: /notes_app
cd backend
uvicorn main:app --reload

The FastAPI service will start at: http://127.0.0.1:8000

B. Start the Streamlit Frontend

Open a second terminal and run the Streamlit application.
Bash

# Ensure you are in the project root: /notes_app
cd frontend
streamlit run app.py

The Streamlit UI will open automatically in your browser, typically at: http://localhost:8501

👨‍💻 Usage Instructions

    Authentication: Use the sidebar on the Streamlit app to Signup (creates a user in the local database) and then Login with your credentials.

    Note Creation: Click the "➕ Create New Note" button to enter the editor view.

    Summarization: Once a note is saved, click the "🧠 Summarize with AI" button on the note card. The FastAPI backend will send the content to the Azure OpenAI service, retrieve the summary, and update the note in the database.

📁 Project Structure

notes_app/
├── backend/
│   ├── main.py            # FastAPI main application and routes
│   ├── auth.py            # JWT and password hashing logic
│   ├── models.py          # SQLAlchemy ORM and Pydantic schemas
│   ├── database.py        # SQLAlchemy engine and session setup (SQLite)
│   └── ai_service.py      # AzureOpenAI client and summarization function
├── frontend/
│   └── app.py             # Streamlit UI and API calling logic
├── .env                   # Environment variables (Azure keys, secrets)
├── requirements.txt       # Python dependencies
└── README.md              # This file
That's a great final step! A well-written README.md is essential for any GitHub project, as it acts as the primary documentation and entry point for users and potential contributors.

Here is a complete, professional, and detailed README file tailored specifically for your Azure AI Notes App, including setup instructions for both the FastAPI backend and the Streamlit frontend.

📝 Azure AI Notes App

An end-to-end full-stack application for note-taking featuring secure user authentication (FastAPI, JWT) and intelligent summarization powered by Azure OpenAI Service.

✨ Key Features

    Secure Authentication: User signup and login secured using FastAPI and JSON Web Tokens (JWT).

    Notes Management: Full CRUD (Create, Read, Update, Delete) functionality for managing personal notes.

    AI Summarization: Utilizes Azure OpenAI Service (GPT-4o) to generate concise, 1-3 sentence summaries of long notes with a dedicated API endpoint.

    Modern Stack: Frontend built with Streamlit for rapid development and an interactive UI; Backend built with high-performance FastAPI and SQLAlchemy (SQLite).

🚀 Getting Started

Follow these steps to set up and run the application locally.

1. Prerequisites

You must have Python 3.9+ and pip installed.

2. Project Setup

    Clone the Repository:
    Bash

git clone [YOUR_REPOSITORY_URL]
cd [YOUR_REPOSITORY_NAME]

Create a Virtual Environment (Recommended):
Bash

python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

Install Dependencies:
Bash

    pip install -r requirements.txt

3. Configuration (.env File)

Create a file named .env in the root directory of the project (/notes_app) and populate it with your API keys and a secret key for authentication.
Code snippet

# --- Azure OpenAI Credentials ---
AZURE_OPENAI_API_KEY="7dA5uVLtdvRfQfnxI9M6qV1dFayX0QtLeNmL5QdK6QV4PduYPMBnZQQJ99ALAC5T7U2XJ3w3AAABACOGflMc"
AZURE_OPENAI_ENDPOINT="https://francecentral.api.cognitive.microsoft.com/"
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o" # Must match your deployment name

# --- Authentication Secret ---
SECRET_KEY="YOUR_SUPER_SECURE_JWT_KEY_GENERATE_A_LONG_RANDOM_STRING"

4. Running the Application (Two Terminals Required)

The backend and frontend must run simultaneously.

A. Start the FastAPI Backend

The backend must be run from the root directory to resolve module imports correctly.
Bash

# Ensure you are in the project root: /notes_app
cd backend
uvicorn main:app --reload

The FastAPI service will start at: http://127.0.0.1:8000

B. Start the Streamlit Frontend

Open a second terminal and run the Streamlit application.
Bash

# Ensure you are in the project root: /notes_app
cd frontend
streamlit run app.py

The Streamlit UI will open automatically in your browser, typically at: http://localhost:8501

👨‍💻 Usage Instructions

    Authentication: Use the sidebar on the Streamlit app to Signup (creates a user in the local database) and then Login with your credentials.

    Note Creation: Click the "➕ Create New Note" button to enter the editor view.

    Summarization: Once a note is saved, click the "🧠 Summarize with AI" button on the note card. The FastAPI backend will send the content to the Azure OpenAI service, retrieve the summary, and update the note in the database.

📁 Project Structure

notes_app/
├── backend/
│   ├── main.py            # FastAPI main application and routes
│   ├── auth.py            # JWT and password hashing logic
│   ├── models.py          # SQLAlchemy ORM and Pydantic schemas
│   ├── database.py        # SQLAlchemy engine and session setup (SQLite)
│   └── ai_service.py      # AzureOpenAI client and summarization function
├── frontend/
│   └── app.py             # Streamlit UI and API calling logic
├── .env                   # Environment variables (Azure keys, secrets)
├── requirements.txt       # Python dependencies
└── README.md              # This file

🛠 Built With

    Python 3.10+

    FastAPI - Backend API Framework

    Streamlit - Frontend UI Library

    SQLAlchemy - ORM for SQLite database

    Azure OpenAI Service - AI Summarization via GPT-4o

    
