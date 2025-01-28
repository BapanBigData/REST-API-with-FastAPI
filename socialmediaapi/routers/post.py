from fastapi import APIRouter

# Import necessary models for post handling from local package
from socialmediaapi.models.post import UserPost, UserPostIn

router = APIRouter()  # Initialize a new instance of the API Router

# Define an in-memory data storage for posts (will be replaced with a database in production)
post_table = {}


# Define POST /post endpoint with UserPost response model
@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    if not post:
        return {"error": "Invalid input"}

    data = post.model_dump()  # Serialize request object to a dictionary

    # Get the number of records currently stored in the table
    last_record_id = len(post_table)
    # Create a new post object with the generated ID and stored data
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post  # Add new post to the table

    return new_post


# Define GET /post endpoint with UserPost list response model
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    if not post_table:
        return []

    return list(post_table.values())
