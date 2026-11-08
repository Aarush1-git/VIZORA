from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.routers import auth

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}

