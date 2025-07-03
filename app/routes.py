from fastapi import APIRouter, HTTPException
from app.models import User
from app.database import db
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.post("/users", status_code=201)
async def create_user(user: User):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.model_dump()
    user_dict["birthdate"] = user_dict["birthdate"].isoformat()
    result = await db.users.insert_one(user_dict)
    
    # Criar resposta limpa sem ObjectId
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email,
        "birthdate": user.birthdate.isoformat()
    }

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["id"] = str(user["_id"])
    del user["_id"]
    return user

@router.get("/users")
async def get_all_users():
    users = await db.users.find().to_list(100)
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    return users

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    try:
        existing_user = await db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    email_check = await db.users.find_one({"email": user.email, "_id": {"$ne": ObjectId(user_id)}})
    if email_check:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.model_dump()
    user_dict["birthdate"] = user_dict["birthdate"].isoformat()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    
    # Criar resposta limpa sem ObjectId
    return {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "birthdate": user.birthdate.isoformat()
    }

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}
