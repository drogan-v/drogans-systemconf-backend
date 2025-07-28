from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import get_object_or_404
from app.db.models.user import User
from app.db.session import get_db_session
from app.schemas.user import UserResponse

router = APIRouter(prefix="", tags=["User"])


@router.get(
    "/users",
    response_model=list[UserResponse],
    description="Get all users",
    summary="Get all users",
)
async def get_users(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User))
    users = get_object_or_404(result.scalars().all(), detail="Users not found")
    return users


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    description="Get user by user_id",
    summary="Get user",
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = get_object_or_404(result.scalar_one_or_none(), detail="User not found")
    return user
