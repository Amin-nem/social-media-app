from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, post,user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)