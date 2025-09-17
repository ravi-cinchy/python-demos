from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# Change relative imports to absolute imports
import crud
import models
from database import SessionLocal, engine
from datetime import datetime

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration API", version="1.0.0")

# Add CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=models.UserResponse)
async def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="🚫 Oops! This email is already registered! 😊 Please use a different email or login instead. 💌"
        )
    
    # Create new user
    db_user = crud.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    return models.UserResponse(
        id=db_user.id,
        full_name=db_user.full_name,
        email=db_user.email,
        phone=db_user.phone,
        created_at=db_user.created_at.isoformat()
    )

@app.get("/users/", response_model=list[models.UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return [
        models.UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at.isoformat()
        )
        for user in users
    ]

@app.get("/")
async def root():
    return {"message": "Welcome to User Registration API! 🎉"}