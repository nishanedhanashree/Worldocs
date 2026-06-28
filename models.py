from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String)
    reset_token = Column(String, nullable=True, index=True)
    reset_token_expiry = Column(DateTime, nullable=True)

class TranslationTask(Base):
    __tablename__ = "translation_tasks"

    id = Column(String, primary_key=True, index=True) # UUID string
    user_id = Column(Integer, index=True)
    original_filename = Column(String)
    target_language = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")
    download_url = Column(String, nullable=True)
