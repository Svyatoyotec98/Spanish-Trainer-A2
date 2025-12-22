from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ========== PROFILES ==========
class ProfileCreate(BaseModel):
    nickname: str
    
class ProfilePublic(BaseModel):
    id: int
    user_id: int
    nickname: str
    created_at: str

class Config:
    from_attributes = True
        
class NavigationState(BaseModel):
    screen_id: str
    current_unidad: str | None = None
    current_category: str | None = None