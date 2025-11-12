from fastapi import FastAPI
from api.users import router as user_router
from services.auth import router as auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}