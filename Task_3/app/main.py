# app/main.py
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes
app.include_router(user.router)
