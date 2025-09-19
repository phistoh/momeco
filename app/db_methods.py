import logging

from db_data import Album, DeclarativeBase
from sqlalchemy import URL, create_engine, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from utils import copy_attributes, get_dict_hash, remove_keys_from_dict

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

KEYS_TO_REMOVE = {"_sa_instance_state", "hash", "id"}


def connect_to_db() -> Session | None:
    url = "sqlite:///local_albums.db"

    try:
        engine = create_engine(url)
        DeclarativeBase.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

    except OperationalError as err:
        session = None
        logger.error("%s", err)

    return session


def save_to_db(
    session: Session,
    album: dict,
) -> int:
    """Internal method used to actually write data to the database.
    session is the session to use and data the data to save.
    """

    data_for_db = Album()
    copy_attributes(album, data_for_db)

    row_hash = get_dict_hash(album)
    query_result = session.query(Album).filter_by(hash=row_hash).first()

    if query_result:
        logger.warning("%s - %s (%s) already in database with id %s", data_for_db.artist, data_for_db.album, data_for_db.mediatype, query_result.id)
        return query_result.id

    data_for_db.hash = row_hash
    session.add(data_for_db)
    session.flush()
    return data_for_db.id


def save_to_db_wrapper(album: dict) -> bool:
    success = True
    session = connect_to_db()

    if session is None:
        success = False
    else:
        save_to_db(session, album)
        session.commit()
    return success


def get_album(artist: str, album: str, mediatype: str) -> list:
    session = connect_to_db()
    albums = []

    if session:
        query_results = session.scalars(
            select(Album)
            .filter(
                Album.artist.ilike(f"%{artist}%"),
                Album.album.ilike(f"%{album}%"),
                Album.mediatype.ilike(f"%{mediatype}%"),
            )
            .order_by(Album.id)
        ).all()
        for query_result in query_results:
            entry = query_result.asdict()
            albums.append(entry)

    return albums


def get_favorites(artist: str, album: str, mediatype: str) -> list:
    session = connect_to_db()
    albums = []

    if session:
        query_results = session.scalars(
            select(Album)
            .where(Album.favorite)
            .filter(
                Album.artist.ilike(f"%{artist}%"),
                Album.album.ilike(f"%{album}%"),
                Album.mediatype.ilike(f"%{mediatype}%"),
            )
            .order_by(Album.id)
        ).all()
        for query_result in query_results:
            entry = query_result.asdict()
            albums.append(entry)

    return albums
