from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine ,SessionLocal,get_db

models.Base.metadata.create_all(bind=engine)



app=FastAPI()




class Post(BaseModel):
    title : str
    content : str
    published: bool =True
    
while True: 
    try:
        conn=psycopg2.connect(host ='localhost',database='fastapi',user='postgres',password='Rajasri@123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection successfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error was: ", error)
        time.sleep(2)


my_posts=[{"title": "title of post 1","content":"content of post 1","id":1},{"title":"favourite food","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    new_post=cursor.fetchone()

    conn.commit()
    return {"Data":new_post}

@app.get("/posts/{id}")
def get_post(id: int ):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    post=cursor.fetchone()    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with the id you mentioned not found")
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int,status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute("""DELETE FROM posts WHERE id= %s returning  * """,(str(id),) )
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with the id you mentioned not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    cursor.execute(""" UPDATE posts SET title =%s,content =%s ,published= %s WHERE id = %s RETURNING * """,
                   (post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with the id you mentioned not found")
    
    
    return {"data":updated_post}