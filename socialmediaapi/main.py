from fastapi import FastAPI

# Import necessary models for post handling
from socialmediaapi.models.post import UserPost, UserPostIn

# Initialize FastAPI application instance
app = FastAPI()

# In-memory data storage for posts (will be replaced with a database in production)
post_table = {}

# Define API endpoint to create a new post
@app.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    """
    Create a new post.

    Args:
        post (UserPostIn): Post data

    Returns:
        UserPost: Created post object
    """

    # Validate incoming request data
    if not post:
        return {"error": "Invalid input"}

    # Convert request object to dictionary for storage
    data = post.model_dump()

    # Generate a unique ID for the new post
    last_record_id = len(post_table)

    # Create a new post object with the generated ID and stored data
    new_post = {**data, "id": last_record_id}

    # Store the new post in the table
    post_table[last_record_id] = new_post

    return new_post


# Define API endpoint to retrieve all posts
@app.get("/post", response_model=list[UserPost])
async def get_all_posts():
    """
    Retrieve a list of all posts.

    Returns:
        list[UserPost]: List of all post objects
    """

    # Return an empty list if no posts are stored
    if not post_table:
        return []

    # Return a list of all posts in the table as UserPost objects
    return list(post_table.values())
