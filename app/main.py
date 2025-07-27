from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine, Base, get_async_session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    ### Create database without migrations ###
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    ### ---------------------------------- ###
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def db_access(db: AsyncSession = Depends(get_async_session)):
    return {"status": "ok"}