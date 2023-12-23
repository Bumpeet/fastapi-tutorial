from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True

class GetUserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostCreate(PostBase):
    # user_id: int
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    # user: GetUserResponse

class PostResponseWithVotes(PostBase):
    Post: PostResponse
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    email: EmailStr



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    # user_id: int

class VoteSchema(BaseModel):
    post_id: int
    direction: int
