# Python Demos

- Create a python project using python uv package manager.
- I want to use this virtaul env for all other demo projects.


Project 1 - Pydantic Python Project Overview

- In pydantic folder create a new project
- Using pydantic/fastapi/streamlist and a database create a simple app that will take user details from UI, perform validations and store it in database.
- If the same user tries to register again and then throw a frienly messages with emojis.

Pydantic/
├── api/                # FastAPI backend
│   ├── __init__.py
│   ├── main.py         # FastAPI app and endpoints
│   ├── models.py       # Pydantic models
│   ├── crud.py         # Database operations (Create, Read, etc.)
│   └── database.py     # Database connection and setup
│
├── ui/                 # Streamlit frontend
│   ├── __init__.py
│   └── app.py          # The Streamlit UI code
│
└── pyproject.toml      # Project dependencies for uv

## Setup & Run

Install dependencies (uses `uv.lock`):

```powershell
cd "c:\Users\Ravi Putcha\Desktop\python-demos\Pydantic"
uv sync --frozen
```

Run the FastAPI backend (recommended from project root):

```powershell
cd "c:\Users\Ravi Putcha\Desktop\python-demos\Pydantic"
uv run uvicorn api.main:app --reload
```

Alternative (from api folder):

```powershell
cd "c:\Users\Ravi Putcha\Desktop\python-demos\Pydantic\api"
uv run uvicorn main:app --reload
```

Run the Streamlit UI:

```powershell
cd "c:\Users\Ravi Putcha\Desktop\python-demos\Pydantic\ui"
uv run streamlit run app.py
```

Open API docs at <http://localhost:8000/docs> and Streamlit at the URL shown (usually <http://localhost:8501>).
