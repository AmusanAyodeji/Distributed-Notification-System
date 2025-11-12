from fastapi import FastAPI
from api.templates import router as templates_router
from api.health import router as health_router

app = FastAPI()

app.include_router(templates_router)
app.include_router(health_router)
