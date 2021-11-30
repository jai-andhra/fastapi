from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes",
                    tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VotesResponse, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist!")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user.id)
    found_vote = vote_query.first()

    print(found_vote)

    if (vote.direction == 1):
            if (found_vote):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user.id} has already voted on post {vote.post_id}")
            else:
                new_vote = models.Votes(user_id = user.id, post_id = vote.post_id)        
                db.add(new_vote)
                db.commit()

                return {"message": {"successfully added vote"}}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist!")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": {"successfully deleted vote"}}
