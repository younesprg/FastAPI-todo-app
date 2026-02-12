from fastapi import FastAPI, Depends, HTTPException, status, Path, APIRouter
from database import engine, SessionLocal
from typing import Annotated
from models import Todos
from pydantic import BaseModel, Field
import models
from sqlalchemy.orm import  Session
from routers import auth, todos

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]   ##dependency enjection



class TodoRequst(BaseModel):
    title: str = Field(min_length= 3)
    description: str =Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 
    
    

@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()



@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency, todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Entity not found') 



@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_requets: TodoRequst):
    todo_model = Todos(**todo_requets.model_dump())
    
    db.add(todo_model)
    db.commit()
    


@router.put("/todo/{tofo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      todol_requrst:TodoRequst, 
                      todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todos not found')
    
    todo_model.title=todol_requrst.title
    todo_model.description=todol_requrst.description
    todo_model.priority=todol_requrst.priority
    todo_model.complete=todol_requrst.complete
    
    db.add(todo_model)
    db.commit()
    


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency,todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id== todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    db.delete(todo_model)     ## db.query(Todos).filter(Todos.id== todo_id).delete() (bu da olurdu)
    db.commit()
