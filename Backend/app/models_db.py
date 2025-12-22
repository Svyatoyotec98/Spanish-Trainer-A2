from sqlalchemy import Column, Integer, String
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Profile(Base):
    __tablename__="profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    nickname = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    
class NavigationState(Base):
    __tablename__ = "navigation_states"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    screen_id = Column(String)
    current_unidad = Column(String, nullable=True)
    current_category = Column(String, nullable=True)