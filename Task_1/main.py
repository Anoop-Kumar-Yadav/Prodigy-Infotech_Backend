from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, EmailStr, Field

from uuid import uuid4

app = FastAPI()

users = dict() # Simulate Database

class User(BaseModel):
    name:str = Field(...,min_length=1) # must not empty
    age:int = Field(...,gt=0) # must be greater than 0
    email:EmailStr

@app.post("/users",status_code=201)
def create_user(user:User):
    user_id = str(uuid4())
    users[user_id] = user.model_dump()
    return {"id": user_id, **user.model_dump()}

@app.get("/users")
def get_all_users():
    return [{"id": uid, **data} for uid, data in users.items()]

@app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **users[user_id]}

@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = user.dict()
    return {"id": user_id, **user.dict()}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return

