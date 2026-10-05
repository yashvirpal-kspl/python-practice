from fastapi import APIRouter, Depends, HTTPException,Query
from database import get_session
from sqlmodel import select,Session

from models.user import User, UserCreate, UserRead

from auth import verify_api_key 

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserRead)
def register_user(
    user_data:UserCreate,
    session:Session = Depends(get_session), 
    api_key: str = Depends(verify_api_key)
    ):
    # match the api_key with the one in .env or config file
    if not api_key:
        raise HTTPException(status_code=401,detail="Invalid API Key")
    
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
     
    user = User.model_validate(user_data)
    session.add(user)  
    session.commit()
    session.refresh(user)
    return user

@router.get("/",response_model=list[UserRead])
def list_users(session:Session = Depends(get_session)):
    users = session.exec(select(User)).all()
