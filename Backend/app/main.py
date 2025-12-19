from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from . import models_db
from sqlalchemy.orm import Session

from .models import UserCreate, LoginRequest, Token, UserPublic
from .auth import register_user, login, get_current_user, get_db


app = FastAPI(title="Spanish Trainer API")
 
# CORS: разрешаем фронтенду обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/auth/register", response_model=UserPublic)
def auth_register(payload: UserCreate, db=Depends(get_db)):
    return register_user(payload, db)


@app.post("/auth/login", response_model=Token)
def auth_login(payload: LoginRequest, db=Depends(get_db)):
    return login(payload, db)



@app.get("/me", response_model=UserPublic)
def me(current_user: UserPublic = Depends(get_current_user)):
    return current_user

# ═══════════════════════════════════════════════════════════════
# PROFILES
# ═══════════════════════════════════════════════════════════════

from .models import ProfileCreate, ProfilePublic
from .auth import get_user_profiles, create_user_profile
from typing import List


@app.get("/profiles", response_model=List[ProfilePublic])
def profile_list(
        current_user: UserPublic = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Получить все профили текущего  пользователя"""
    return get_user_profiles(current_user.id, db)
    
@app.post("/profiles", response_model=ProfilePublic)
def profiles_create(
    paylaod: ProfileCreate,
    current_user: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    """Создать новый профиль для текущего пользователя"""
    return create_user_profile(current_user.id, paylaod, db)