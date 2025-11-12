from pydantic import HttpUrl
from typing import Optional
from enum import Enum
import uuid
from pathlib import Path as path
from pydantic import BaseModel

class NotificationType(str, Enum):
    email = "email"
    push = "push"

class UserData(BaseModel):
    name: str
    link: HttpUrl
    meta: Optional[dict]

class NotificationStatus(str, Enum):
    delivered = "delivered"
    pending = "pending"
    failed = "failed"

class NotificationRequest(BaseModel):
    notification_type: NotificationType
    user_id: uuid.UUID | str
    template_code: str | path
    variables: UserData
    request_id: str
    priority: int
    metadata: Optional[dict]