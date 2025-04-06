from fastapi import APIRouter, HTTPException
from socialmediaapi.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    UserPostWithComment
)

# Initialize a new instance of the API Router
router = APIRouter()

# Define an in-memory data storages
post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


# Define POST /post endpoint with UserPost response model
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    if not post:
        return {"error": "Invalid input"}

    data = post.model_dump()  # Serialize request object to a dictionary

    # Get the number of records currently stored in the table
    last_record_id = len(post_table)

    # Create a new post object with the generated ID and stored data
    new_post = {**data, "id": last_record_id}

    post_table[last_record_id] = new_post

    return new_post


# Define GET /post endpoint with UserPost list response model
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():

    if not post_table:
        return []

    return list(post_table.values())


# Define POST /comment endpoint with Comment response model
@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()

    last_record_id = len(comment_table)

    new_comment = {**data, "id": last_record_id}

    comment_table[last_record_id] = new_comment

    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comment_on_post(post_id)
    }
