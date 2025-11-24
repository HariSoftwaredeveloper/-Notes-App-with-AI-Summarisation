# backend/models.py
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
try:
    # Package import (recommended): `from Backend import models`
    from .database import Base  # CRITICAL: Import Base from database.py
except Exception:
    # Module import when running inside `Backend` folder: `python -c "import models"`
    from database import Base

# --- SQLAlchemy ORM Models (Database Tables) ---
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    notes = relationship("NoteDB", back_populates="owner")

class NoteDB(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="notes")

# --- Pydantic Schemas (Request/Response Data) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserCreate(BaseModel):
    email: str
    password: str

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_id: int
    summary: str | None = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
