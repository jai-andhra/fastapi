from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.util import outerjoin
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

router = APIRouter(prefix="/posts",
                    tags=['Posts'])


# @router.get("/", response_model=List[schemas.PostResponse])
#@router.get("/")
@router.get("/", response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int = 10,
                                skip: int = 0, search: Optional[str] = ""):
#     cursor.execute("""select * from posts""")
#     posts = cursor.fetchall()
# #    return {"message": store_posts}

    print (search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # vote_results = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
    #                                     models.Votes, models.Votes.post_id == models.Post.id, 
    #                                     isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    vote_results = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
                                        models.Votes, models.Votes.post_id == models.Post.id, 
                                        isouter=True).group_by(models.Post.id).all()
    print (vote_results)
    print(posts)
    return posts

# @router.get("/myposts", response_model=List[schemas.PostVotes])
@router.get("/myposts")
def get_post(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int = 10,
                                skip: int = 0, search: Optional[str] = ""):
#     cursor.execute("""select * from posts""")
#     posts = cursor.fetchall()
# #    return {"message": store_posts}

    print (user.email)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post).filter(models.Post.user_id == user.id).limit(limit).offset(skip).all()

    vote_results = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
                                        models.Votes, models.Votes.post_id == models.Post.id, 
                                        isouter=True).group_by(models.Post.id).filter(
                                            models.Post.user_id == user.id).limit(limit).offset(skip).all()
    print (vote_results)
    print(posts)

    return vote_results

# @app.get("/posts/latest")
# def get_latest_post(db: Session = Depends(get_db)):
#     post = store_posts[len(store_posts)-1]
#     return {"latest post:": post}

@router.get("/{id}", response_model=schemas.PostResponse)
#def read_item(id: int, q: Optional[str] = None):
#    return {"item_id": id, "q": q}
def read_item(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int = 10,
                                skip: int = 0, search: Optional[str] = ""):
    # post = find_post_fromDB(id)
#    return {"item_id": f"Id you are interested in: {id}"}
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    post = db.query(models.Post).filter(models.Post.id == id).first() # use first instead of all

    vote_results = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
                                        models.Votes, models.Votes.post_id == models.Post.id, 
                                        isouter=True).group_by(models.Post.id).filter(
                                            models.Post.id == id).limit(limit).offset(skip).first()
    print (vote_results)
    print(post)

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"User Id {id} not Authorized to perform the operation!")

    if not post:
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"get_one_post err": f"Invalid Id {id} specified!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid Id {id} specified!")
    return  post

@router.get("/latest", response_model=schemas.PostResponse)
#def read_item(id: int, q: Optional[str] = None):
#    return {"item_id": id, "q": q}
# def read_item(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
def read_item(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int = 10,
                                skip: int = 0, search: Optional[str] = ""):
    # post = find_post_fromDB(id)
#    return {"item_id": f"Id you are interested in: {id}"}
    post = db.query(models.Post).all() # use first instead of all

    if not post:
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"get_one_post err": f"Invalid Id {id} specified!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid Id {id} specified!")
    return  post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#def create_post(payload: dict = Body(...)):
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * """, 
    #     (payload.title, payload.content, payload.published) )
    # post = cursor.fetchone()
    # conn.commit()

#    post = models.Post(title=payload.title, content=payload.content, published=payload.published)
    print (user.email)
    post = models.Post(user_id = user.id, **payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post
#     print (payload.dict())
#     post_dict = payload.dict()
#     post_dict['id'] = randrange(2,100000)
#     store_posts.append(post_dict)
# #    return {"message": f"{payload.title}"}
#     return {"message": post_dict}

@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict["id"] = id
    # print (post_dict)
   
    # index = update_item(id, post_dict)

    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning * """, 
    #         (post.title, post.content, post.published, (str(id))))
    # upd_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    upd_post = post_query.first()
    if upd_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found to update!")

    if upd_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"User Id {id} not Authorized to perform the operation!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

#    print (store_posts[index])
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # ret = delete_item_fromDB(id)
#    ret = delete_item(id)

    ret = db.query(models.Post).filter(models.Post.id == id)

    if ret.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post Id {id} not found!")

    print(ret.first().user_id)
    if ret.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"User Id {id} not Authorized to perform the operation!")

    ret.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


