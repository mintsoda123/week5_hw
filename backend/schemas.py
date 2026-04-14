from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: str
    name: str
    picture: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_premium: bool
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class UsageStatus(BaseModel):
    usage_count: int
    free_limit: int
    is_premium: bool
    remaining: int
    can_access: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class SectionContent(BaseModel):
    id: str
    title: str
    description: str
    content: str
    code_example: Optional[str] = None
    result_description: Optional[str] = None


class CheckoutResponse(BaseModel):
    checkout_url: str
