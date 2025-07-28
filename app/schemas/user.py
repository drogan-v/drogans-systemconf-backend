from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    class Config:
        from_attributes = True
