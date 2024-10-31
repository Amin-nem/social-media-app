from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import IntEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner : UserOut

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : Optional[str] = None



class VoteDirEnum(IntEnum):
    like = 1
    novote = 0
    
class Vote(BaseModel):
    post_id : int
    vote_di : VoteDirEnum