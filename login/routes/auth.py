from fastapi import APIRouter, HTTPException
from models import User
from db import user_collection

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    await user_collection.insert_one(user.dict())
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: User):
    db_user = await user_collection.find_one({"username": user.username})
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
