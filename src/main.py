from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

# connect to db
try:
    connection = psycopg2.connect(database='fastapi',user='postgres',password='Amin1378',host='localhost',cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("--> database connection was successful")
except Exception as e:
    print(e)


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

my_posts = [
    {"title":"title of post 1", "content":"content of post 1", "id": 1},
    {"title":"title of post 2", "content":"content of post 2", "id": 2}
]

def find_post_by_id(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_post_index_by_Id(id):
    for post in my_posts:
        if post['id'] == id:
            return my_posts.index(post)


@app.get("/")
async def root():
    return {"message":"Hello World"}


@app.get('/posts')
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # records = cursor.fetchall()
    records = db.query(models.Post).all()
    return {"message":records}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session=Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'added_post':new_post}


@app.get("/posts/{id}")
def get_post(id: int,db: Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found.")
    return {'post':post}


@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE from posts WHERE id = %s RETURNING *",(str(id),))
    delted_post = cursor.fetchone()
    connection.commit()
    if not delted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post id {id} not found in database")

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post id {id} not found in database")
    connection.commit()
    return {'post':updated_post}


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status':'success'}