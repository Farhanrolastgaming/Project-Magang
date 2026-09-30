from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from config.database import get_db
import core.models as models
from core.deps import get_current_active_admin

router = APIRouter()

class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: str

    class Config:
        from_attributes = True

class WPAccountAdminResponse(BaseModel):
    id: int
    site_name: str
    wp_url: str
    username: str

    class Config:
        from_attributes = True

@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(db: Session = Depends(get_db), admin: models.User = Depends(get_current_active_admin)):
    users = db.query(models.User).all()
    # Convert datetime to string for response
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at.isoformat()
        })
    return result

@router.get("/users/{user_id}/wp_accounts", response_model=List[WPAccountAdminResponse])
def get_user_wp_accounts(user_id: int, db: Session = Depends(get_db), admin: models.User = Depends(get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    accounts = db.query(models.WPAccount).filter(models.WPAccount.user_id == user_id).all()
    return accounts
