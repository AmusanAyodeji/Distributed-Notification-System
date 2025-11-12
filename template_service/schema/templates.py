from pydantic import BaseModel
from typing import Optional

class TemplateCreate(BaseModel):
    code: str
    subject: str
    body: str
    language_code: str = "en"
    version: int = 1

class TemplateUpdate(BaseModel):
    subject: Optional[str]
    body: Optional[str]
    version: Optional[int]
    language_code: Optional[str]

class Template(BaseModel):
    code: str
    subject: str
    body: str
    language_code: str
    version: int
