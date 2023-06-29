from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    token = Column(String, unique=True, nullable=False)


class Audio(Base):
    __tablename__ = "audios"
    id = Column(String, primary_key=True, index=True)
    mp3_file_path = Column(String)
