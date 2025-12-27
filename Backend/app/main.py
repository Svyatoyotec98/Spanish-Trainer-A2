from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from . import models_db
from sqlalchemy.orm import Session

from .models import UserCreate, LoginRequest, Token, UserPublic, NavigationState, ProgressData
from .auth import register_user, login, get_current_user, get_db
from datetime import datetime, timezone


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
    
    
@app.post("/navigation-state")
def save_navigation_state(state: NavigationState, current_user = Depends(get_current_user), db = Depends(get_db)):
    existing = db.query(models_db.NavigationState).filter_by(user_id=current_user.id).first()
    if existing:
        existing.screen_id = state.screen_id
        existing.current_unidad = state.current_unidad
        existing.current_category = state.current_category
    else:
        new_state = models_db.NavigationState(
            user_id=current_user.id,
            screen_id=state.screen_id,
            current_unidad=state.current_unidad,
            current_category=state.current_category
        )
        db.add(new_state)
    db.commit()
    return {"ok": True}
    
@app.get("/navigation-state")
def get_navigation_state(current_user = Depends(get_current_user), db = Depends(get_db)):
    state = db.query(models_db.NavigationState).filter_by(user_id=current_user.id).first()
    if not state:
        return None
    return {
        "screen_id": state.screen_id,
        "current_unidad": state.current_unidad,
        "current_category": state.current_category
    }
    
@app.post("/progress")
def save_progress(payload: ProgressData, current_user = Depends(get_current_user), db = Depends(get_db)):
    existing = db.query(models_db.Progress).filter_by(user_id=current_user.id).first()
    if existing:
        existing.data = payload.data
        existing.updated_at = datetime.now(timezone.utc).isoformat()
    else:
        new_progress = models_db.Progress(
            user_id=current_user.id,
            data=payload.data,
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        db.add(new_progress)
    db.commit()
    return{"ok": True}


@app.get("/progress")
def get_progress(current_user = Depends(get_current_user), db = Depends(get_db)):
    progress = db.query(models_db.Progress).filter_by(user_id=current_user.id).first()
    if not progress:
        return None
    return{"data": progress.data}

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
    payload: ProfileCreate,
    current_user: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    """Создать новый профиль для текущего пользователя"""
    return create_user_profile(current_user.id, paylaod, db)