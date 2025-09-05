from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
