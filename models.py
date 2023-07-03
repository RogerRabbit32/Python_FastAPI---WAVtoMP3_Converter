from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    token = Column(String, unique=True, nullable=False)

    audios = relationship("Audio", back_populates="owner")


class Audio(Base):
    __tablename__ = "audios"
    id = Column(String, primary_key=True, index=True)
    mp3_file_path = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="audios")
