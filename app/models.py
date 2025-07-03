from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    birthdate: date

class UserInDB(User):
    id: Optional[str]
