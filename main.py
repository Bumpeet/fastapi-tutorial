from fastapi import FastAPI

from files import models
from files.database import engine
from files.routers import posts, users, auth, vote
from files.config import Settings

from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)



settings = Settings()

origins =[
    'https://www.postman.com'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# while True:
#     try:
#         conn = psycopg2.connect(database="fastapi",
#                                 user = "postgres",
#                                 password = "Phetas@123",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection sucess")
#         break
        
#     except Exception as e:
#         print("connection didn't happen check your params")
#         print(e)
#         time.sleep(5)

# class Post(BaseModel):
#     title: str
#     description: str
#     published: bool = True # this will default to True even if we don't pass this in the body of post request
#    # rating: Optional[int] = None # if user wants to send then they can send or else no need of this parameter to be passed


# @app.get("/sqlalchemy")
# def test_posts(db: Session=Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts


    
