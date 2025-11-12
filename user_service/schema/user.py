from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import HttpUrl
from enum import Enum
import uuid
from pathlib import Path as path

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

class UserData(BaseModel):
    name: str
    link: HttpUrl | str
    meta: Optional[dict]

class NotificationType(str, Enum):
    email = "email"
    push = "push"

class NotificationRequest(BaseModel):
    notification_type: NotificationType
    user_id: uuid.UUID | str
    template_code: str | path
    variables: UserData
    request_id: str
    priority: int
    metadata: Optional[dict]