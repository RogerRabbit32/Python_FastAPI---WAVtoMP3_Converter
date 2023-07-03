import io
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydub import AudioSegment

from models import User, Audio


def validate_user(db: Session, user_id: int, access_token: str):
    # Checks the user access credentials
    user = db.query(User).filter(User.id == user_id, User.token == access_token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")


async def convert_audio(db: Session, audio):
    audio_id = str(uuid4())

    # Converts WAV to MP3 and saves the resulting file to ./audios/media
    audio_bytes = await audio.read()
    audio_file = io.BytesIO(audio_bytes)
    audio_segment = AudioSegment.from_file(audio_file, format='wav')
    audio_path = f"Audios/media/{audio_id}.mp3"
    audio_segment.export(audio_path, format='mp3')

    # Saves the audio path to db
    new_audio = Audio(id=audio_id, mp3_file_path=audio_path)
    db.add(new_audio)
    db.commit()
    db.close()

    return audio_id
