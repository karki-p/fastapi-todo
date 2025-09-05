from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoOut

router = APIRouter(prefix="/api/todos", tags=["todos"])

@router.get("", response_model=List[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.id.desc()).all()

@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(title=payload.title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if payload.title is not None:
        todo.title = payload.title
    if payload.completed is not None:
        todo.completed = payload.completed

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return None
