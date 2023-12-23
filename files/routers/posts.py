from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..models import *
from ..schemas import *
from ..database import get_db
from ..oauth2 import create_access_token, get_current_user


router = APIRouter(prefix="/posts",
                   tags=["Posts"])

@router.get("/", )
def get_posts(db: Session=Depends(get_db), 
              token_data:TokenData = Depends(get_current_user),
              search: Optional[str]="",
              limit: int = 10,
              offset: int = 0):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(Post, func.count(Post.id).label("votes")).\
        join(Votes, Post.id==Votes.post_id, isouter=True).group_by(Post.id).\
        filter(Post.title.contains(search)).limit(limit).offset(offset)
    print(posts)
    return posts.all()

@router.post("/", 
          status_code=status.HTTP_201_CREATED, 
          response_model=PostResponse)
def create_posts(post: PostCreate, db: Session=Depends(get_db),
                 user: GetUserResponse = Depends(get_current_user)):
    # print(post.model_dump())
    # cursor.execute("""
    #                 INSERT INTO posts (title, content, publish) VALUES
    #                (%s,%s, %s) RETURNING *
    #                 """,
    #                 (post.title, post.content, post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(token_data)
    # print("=====",user.id)
    # print("____",post.model_dump())
    new_post = Post(**post.model_dump(),user_id=user.id)
    # new_post = Post(title=post.title, description=post.description, published=post.published) 
    db.add(new_post)
    db.commit() 
    db.refresh(new_post) #Returning *
    # print(new_post) #returns class
    return new_post

@router.get("/{id}", response_model=PostResponse,)
def get_post(id:int, db: Session=Depends(get_db),
             user: GetUserResponse = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""", (str(id)))
    # post = cursor.fetchall()
    post = db.query(Post).filter(Post.id==id).first() #.all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"the requested id-{id} is not present in our system")
    return post

@router.delete("/{id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            )
def delete_post(id:int, db: Session=Depends(get_db),
                user: GetUserResponse = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    post = db.query(Post).filter(Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=404, detail=f'did not find the post-{id}')
    if post.first().user_id==user.id:
        # conn.commit()
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'you are not authorized to delete this post')

@router.put("/{id}")
def update_post(id:int, post: PostCreate, db:Session=Depends(get_db),
                user: GetUserResponse = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts set title=%s, content=%s where id=%s RETURNING *""", (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # if updated_post==None:
    #     raise HTTPException(status_code=404, detail=f'did not find the post-{id}')
    # conn.commit()
    post_query = db.query(Post).filter(Post.id==id)
    if post_query.first()==None:
        raise HTTPException(status_code=404, detail=f'did not find the post-{id}')
    print(f'postid-{post_query.first().user_id} and userid-{user.id}')
    if post_query.first().user_id==user.id:

        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'you cannot update this post')
