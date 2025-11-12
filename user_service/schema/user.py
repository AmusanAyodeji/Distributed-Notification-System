from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPreference(BaseModel):
    email: bool
    push: bool

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    push_token: Optional[str]
    preferences: UserPreference
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    push_token: Optional[str]
    preferences: Optional[UserPreference]
    password: Optional[str]

class UserOut(BaseModel):
    name: str
    email: EmailStr
    push_token: Optional[str]
    preferences: UserPreference
