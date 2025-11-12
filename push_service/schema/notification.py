from pydantic import BaseModel
from typing import Optional, Dict

class NotificationData(BaseModel):
    title: str
    body: str
    image: Optional[str] = None
    link: Optional[str] = None
    meta: Optional[Dict] = None
