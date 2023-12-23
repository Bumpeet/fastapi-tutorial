from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import VoteSchema, GetUserResponse
from ..models import Votes, Post

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(payload:VoteSchema, 
              db:Session = Depends(get_db),
              auth_user:GetUserResponse = Depends(get_current_user)):
    user_id = auth_user.id
    post_id = payload.post_id
    direction = payload.direction

    post_query = db.query(Post).filter(Post.id==post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post-{post_id} doesn't exit")
    query = db.query(Votes).filter(Votes.user_id==user_id, Votes.post_id==post_id)

    if query.first() is None:
        if direction==1:
            new_vote = Votes(user_id=user_id, post_id=post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return 'added like to the post'
        
        elif direction==0:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail=f'already disliked this post')
    else:
        if direction==0:
            query.delete(synchronize_session=False)
            db.commit()
            return 'removed your like'
        elif direction==1:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                                detail=f'already liked')

