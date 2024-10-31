from fastapi import status, HTTPException, Depends, APIRouter
from .. import models,schema, oauth2, database
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote:schema.Vote, db: Session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_exist = vote_query.first()
    if vote.dir == 1:
        if vote_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f" user with user id {current_user.id} has already voted on the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, vote_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully liked."}
    else:
        if not vote_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"vote doesn't exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully delete like."}