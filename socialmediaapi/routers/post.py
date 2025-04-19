from fastapi import APIRouter, HTTPException
from socialmediaapi.database import post_table, comment_table, database
from socialmediaapi.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    UserPostWithComment
)

# Initialize a new instance of the API Router
router = APIRouter()



async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


# Define POST /post endpoint with UserPost response model
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()  
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)

    return {**data, "id": last_record_id}


# Define GET /post endpoint with UserPost list response model
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)



# Define POST /comment endpoint with Comment response model
@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)

    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comment_on_post(post_id)
    }
