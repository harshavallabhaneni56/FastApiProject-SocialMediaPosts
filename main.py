from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app=FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool =True
    rating: Optional[int]= None
    

my_posts=[{"title": "title of post 1","content":"content of post 1","id":1},{"title":"favourite food","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"Data":post_dict}

@app.get("/posts/{id}")
def get_post(id: int ):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with the id you mentioned not found")
    return {"post_detail": post}