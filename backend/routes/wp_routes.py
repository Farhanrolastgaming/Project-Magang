from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from config.database import get_db
import core.models as models
from core.deps import get_current_user

router = APIRouter()

class WPAccountCreate(BaseModel):
    site_name: str
    wp_url: str
    username: str
    app_password: str

class WPAccountResponse(BaseModel):
    id: int
    site_name: str
    wp_url: str
    username: str
    # Do not return app_password

    class Config:
        from_attributes = True

@router.get("/", response_model=List[WPAccountResponse])
def get_wp_accounts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    accounts = db.query(models.WPAccount).filter(models.WPAccount.user_id == current_user.id).all()
    return accounts

@router.post("/", response_model=WPAccountResponse)
def add_wp_account(account_in: WPAccountCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Task 1.2: Limit to 10 accounts per user
    count = db.query(models.WPAccount).filter(models.WPAccount.user_id == current_user.id).count()
    if count >= 10:
        raise HTTPException(status_code=400, detail="Maximum limit of 10 WordPress accounts reached.")
    
    new_account = models.WPAccount(
        user_id=current_user.id,
        site_name=account_in.site_name,
        wp_url=account_in.wp_url,
        username=account_in.username,
        app_password=account_in.app_password
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.delete("/{account_id}")
def delete_wp_account(account_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    account = db.query(models.WPAccount).filter(models.WPAccount.id == account_id, models.WPAccount.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found or access denied.")
    db.delete(account)
    db.commit()
    return {"message": "Account successfully deleted"}
