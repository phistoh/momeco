from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

DeclarativeBase = declarative_base()


class Album(DeclarativeBase):
    """Database model to represent albums."""
    __tablename__ = "Albums"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hash: Mapped[str] = mapped_column(String)

    artist: Mapped[str] = mapped_column(String)
    album: Mapped[str] = mapped_column(String)
    mediatype: Mapped[str] = mapped_column(String)
    favorite: Mapped[bool] = mapped_column(Boolean)

    def asdict(self):
        return {
            "artist": self.artist,
            "album": self.album,
            "mediatype": self.mediatype,
            "favorite": self.favorite,
        }

class Game(DeclarativeBase):
    """Database model to represent albums."""
    __tablename__ = "Games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hash: Mapped[str] = mapped_column(String)

    title: Mapped[str] = mapped_column(String)
    platform: Mapped[str] = mapped_column(String)
    progress: Mapped[int] = mapped_column(Integer)
    favorite: Mapped[bool] = mapped_column(Boolean)

    def asdict(self):
        return {
            "title": self.artist,
            "platform": self.album,
            "progress": self.mediatype,
            "favorite": self.favorite,
        }
