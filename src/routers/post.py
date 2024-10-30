from fastapi import status, HTTPException, Depends, APIRouter
from .. import models,schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List 
from ..oauth2 import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get('/',response_model=List[schema.PostResponse])
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(get_current_user),limit:int=10,skip:int = 0,search:Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # records = cursor.fetchall()
    records = db.query(models.Post).filter(models.Post.owner_id == current_user.id,models.Post.title.contains(search )).limit(limit).offset(skip).all()
    return records

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post:schema.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    print('---->>>',current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",response_model=schema.PostResponse)
def get_post(id: int,db: Session=Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found.")
    return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("DELETE from posts WHERE id = %s RETURNING *",(str(id),))
    # delted_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {id} not found in database")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not autherized to perform requested actions")
    
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}",response_model=schema.PostResponse)
def update_post(id:int, post:schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {id} not found in database")
    
    if query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not autherized to perform requested actions")
    # connection.commit()
    query.update(post.dict(),synchronize_session=False)
    db.commit()
    return query.first()