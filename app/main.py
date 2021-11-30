from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from app.routers import vote
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote

from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://www.google.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

app.include_router(post.router)

app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "My World"}


# USE THIS if connecting to POSTGRES DB directly
# THIS CODE USES SQLACHEMY to connect
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print ("Database connection successful!")
#         break
#     except Exception as error:
#         print("DB Connection failed.")
#         print("Error", error)
#         time.sleep(2)


# store_posts = [{"title": "Title of post", "content": "Content of Post", "id": 1}, {"title": "Title of foods","content": "Food content", "id": 2}]

# def find_post_fromDB(id):
#     cursor.execute("""select * from posts where id = %s """, (str(id)) )
#     post = cursor.fetchone()

#     return post

# def find_post(id):
#     for p in store_posts:
#         if p["id"] == id:
#             return p

# def delete_item_fromDB(id):
#     cursor.execute("""delete from posts where id = %s returning * """, (str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#     return post

#     # for p in store_posts:
#     #     if p["id"] == id:
#     #         store_posts.remove(p)
#     #         return id
#     return 0            

# def delete_item(id):
#     for p in store_posts:
#         if p["id"] == id:
#             store_posts.remove(p)
#             return id
#     return 0            

# def update_item(id, post):
#     for i, p in enumerate(store_posts):
#         if p["id"] == id:
#             store_posts[i]= post
#             return i
             

