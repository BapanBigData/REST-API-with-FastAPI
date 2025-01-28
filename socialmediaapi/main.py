from fastapi import FastAPI

from socialmediaapi.routers.post import router as post_router

# Initialize FastAPI application instance
app = FastAPI()

app.include_router(post_router)
