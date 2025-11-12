from fastapi import APIRouter, Body, HTTPException
from schema.templates import TemplateCreate
from services.crud import create_template, get_template_by_code, fill_template

router = APIRouter()

@router.post("/api/v1/templates/")
def create_template_endpoint(template: TemplateCreate = Body(...)):
    db_t = create_template(template.model_dump())
    return {
        "success": True, 
        "message": "Template created", 
        "data": db_t, 
        "meta": {}
        }

@router.post("/api/v1/templates/fill/")
def get_filled_template(code: str, variables: dict, language_code: str = "en"):
    db_t = get_template_by_code(code, language_code)
    if not db_t:
        raise HTTPException(status_code=404, detail="Template not found")
    filled = fill_template(db_t.body, variables)
    return {
        "success": True, 
        "data": {"subject": db_t.subject, "body": filled}, 
        "message": "Template filled", 
        "meta": {}
        }
