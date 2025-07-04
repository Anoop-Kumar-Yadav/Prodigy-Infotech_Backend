from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import user 
from app.routes import protected


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="JWT Auth API",
    description="Backend Auth System using FastAPI + JWT + SQLAlchemy",
    version="1.0.0"
)
app.include_router(protected.router)
app.include_router(user.router)
