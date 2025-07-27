from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True
