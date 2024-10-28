from fastapi import status, HTTPException, Depends, APIRouter
from .. import models,schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get('/posts',response_model=List[schema.PostResponse])
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # records = cursor.fetchall()
    records = db.query(models.Post).all()
    return records

@router.post('/posts',status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post:schema.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/posts/{id}",response_model=schema.PostResponse)
def get_post(id: int,db: Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found.")
    return post


@router.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE from posts WHERE id = %s RETURNING *",(str(id),))
    # delted_post = cursor.fetchone()
    # connection.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {id} not found in database")
    
    query.delete(synchronize_session=False)
    db.commit()

@router.put("/posts/{id}",response_model=schema.PostResponse)
def update_post(id:int, post:schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {id} not found in database")
    # connection.commit()
    query.update(post.dict(),synchronize_session=False)
    db.commit()
    return query.first()


@router.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {'status':'success'}