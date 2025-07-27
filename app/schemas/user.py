from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True
