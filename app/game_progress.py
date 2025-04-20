# game_progress.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

try:
    from app.database import get_db
    from app.models import User
except ImportError:
    # Fix the relative imports to use the correct path
    from .database import get_db
    from .models import User

router = APIRouter(
    prefix="/progress",
    tags=["Game Progress"]
)

# Schema for updating progress
class ProgressUpdate(BaseModel):
    current_module: str
    current_chapter: int

@router.patch("/update", response_model=ProgressUpdate)
def update_progress(
    progress_update: ProgressUpdate,
    user_email: str = Query(..., description="Email of the user to update"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.progress = progress_update.dict()
    db.commit()
    db.refresh(user)
    return progress_update

@router.get("/current", response_model=ProgressUpdate)
def get_current_progress(
    user_email: str = Query(..., description="Email of the user"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # If progress is empty, return a default progress
    default_progress = {"current_module": "", "current_chapter": 0}
    return user.progress or default_progress
