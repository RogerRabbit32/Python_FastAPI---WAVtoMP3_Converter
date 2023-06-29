from pydantic import BaseModel
from fastapi import UploadFile, File


class AudioUpload(BaseModel):
    user_id: int
    user_access_token: str
    audio: UploadFile
