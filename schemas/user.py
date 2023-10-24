from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    image_url: Optional[str] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    username: str
    email: EmailStr
    password: str
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
