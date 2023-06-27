from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from Accounts.schemas import UserCreate, UserResponse
from database import SessionLocal, engine
from models import Base, User

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user", response_model=UserResponse)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    new_user_token = uuid4()

    # Check if the token already exists in the database
    if db.query(User).filter(User.token == new_user_token).first():
        raise HTTPException(status_code=422, detail="Couldn't generate user token. Please try again")

    new_user = User(name=request.name, token=new_user_token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(id=new_user.id, token=str(new_user.token))
