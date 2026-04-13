from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Enterprise User API", version="1.0.0")


# --- Schemas (Data Validation) ---
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


# Mock Database
users_db = {}


# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "Welcome to the Production API"}


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    """
    Creates a new user. FastAPI automatically validates the
    request body against the 'User' Pydantic model.
    """
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.id] = user
    return user


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user