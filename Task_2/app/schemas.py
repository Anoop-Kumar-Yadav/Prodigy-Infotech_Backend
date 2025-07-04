
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserOut(UserCreate):
    id: str

    model_config = {
        "from_attributes": True 
    }
