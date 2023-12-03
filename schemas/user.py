from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: constr(min_length=8)

    @validator('password')
    def password_validation(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserNewPassword(BaseModel):
    otp: str
    email: EmailStr
    password: str


class UserSendVerify(BaseModel):
    email: EmailStr


class UserVerifyEmail(BaseModel):
    email: EmailStr
    otp: str


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


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
