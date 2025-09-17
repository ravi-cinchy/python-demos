from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# SQLAlchemy Model (Database)
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic Models (API)
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip().title()
    
    @validator('phone')
    def validate_phone(cls, v):
        # Simple phone validation - adjust as needed
        phone_digits = ''.join(filter(str.isdigit, v))
        if len(phone_digits) not in [10, 11]:
            raise ValueError('Phone number must be 10 or 11 digits')
        return phone_digits

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True