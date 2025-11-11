from api.notification import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
