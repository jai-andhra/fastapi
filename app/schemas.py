from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.models import Post


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse
    
    class Config:
        orm_mode = True

# class Post(PostResponse):
#     pass

class PostVotes(BaseModel):
    post: PostResponse
    vote: int



class VotesResponse(BaseModel):
        post_id: int
        direction: conint(le=1)