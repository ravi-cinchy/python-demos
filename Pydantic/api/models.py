from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

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

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip().title()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        phone_digits = ''.join(filter(str.isdigit, v))
        if len(phone_digits) not in [10, 11]:
            raise ValueError('Phone number must be 10 or 11 digits')
        return phone_digits

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)