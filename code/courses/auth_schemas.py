from ninja import Schema
from pydantic import field_validator, Field
from typing import Optional
import re

class RegisterSchema(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: str
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email tidak valid')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password minimal 8 karakter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung huruf besar')
        return v


class LoginSchema(Schema):
    username: str
    password: str


class TokenResponseSchema(Schema):
    access: str
    refresh: str
    user: dict


class MessageSchema(Schema):
    message: str
    detail: Optional[str] = None
