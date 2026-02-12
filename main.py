from fastapi import FastAPI
from models import Todos
from pydantic import BaseModel, Field
import models
from sqlalchemy.orm import  Session
from routers import auth, todos
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

