from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydub import AudioSegment
from uuid import uuid4
import io

from Accounts.schemas import UserCreate, UserResponse
from database import SessionLocal, engine
from models import Base, User, Audio

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
    new_user_token = str(uuid4())

    # Check if the token already exists in the database
    if db.query(User).filter(User.token == new_user_token).first():
        raise HTTPException(status_code=422, detail="Couldn't generate user token. Please try again")

    new_user = User(name=request.name, token=new_user_token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/record")
async def convert_audio(user_id: int, user_access_token: str, audio: UploadFile = File(...), db: Session = Depends(get_db)):
    audio_id = str(uuid4())

    # Convert WAV to MP3 and save the resulting file to ./audios/media
    audio_bytes = await audio.read()
    audio_file = io.BytesIO(audio_bytes)
    audio_segment = AudioSegment.from_file(audio_file, format='wav')
    audio_segment.export(f"Audios/media/{audio_id}", format='mp3')

    # Save a new audio object in the DB
    # new_audio = Audio(id=audio_id, mp3_file_path=audio_path)
    # db.add(new_audio)
    # db.commit()
    # db.close()

    # Generate the URL
    url = f"http://localhost:8000/record?id={audio_id}&user={user_id}"
    return {"url": url}
