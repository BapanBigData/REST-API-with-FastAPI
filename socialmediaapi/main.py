from fastapi import FastAPI
from contextlib import asynccontextmanager
from socialmediaapi.routers.post import router as post_router
from socialmediaapi.database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


# Initialize FastAPI application instance
app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
