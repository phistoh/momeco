import json
import logging
from wsgiref.simple_server import WSGIRequestHandler, make_server

from db_methods import get_album, get_favorites, save_to_db_wrapper
from flask import Flask, request

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

app = Flask(__name__)

ALLOWED_MEDIATYPES = {"cd", "digital", "vinyl", "cassette"}


@app.route("/music/getalbum", methods=["GET"])
def return_album():
    artist = request.args.get("artist", default="", type=str)
    album = request.args.get("album", default="", type=str)
    if artist == "" and album == "":
        return "Empty search string not allowed.", 400
    media_type = request.args.get("media_type", default="", type=str)
    res = get_album(artist, album, media_type)
    if res:
        return json.dumps(res, indent=4, sort_keys=True, default=str), 200
    else:
        return [], 404


@app.route("/music/getfavorites", methods=["GET"])
def return_favorites():
    artist = request.args.get("artist", default="", type=str)
    album = request.args.get("album", default="", type=str)
    media_type = request.args.get("media_type", default="", type=str)
    res = get_favorites(artist, album, media_type)
    if res:
        return json.dumps(res, indent=4, sort_keys=True, default=str), 200
    else:
        return [], 404


@app.route("/music/addalbum", methods=["POST"])
def save_album():
    album = request.json
    if album:
        artist = album.get("artist", "")
        album_title = album.get("album", "")
        mediatype = album.get("mediatype", "").lower()
        if artist == "" or album_title == "" or mediatype == "":
            return "Album without artist, album name or media type not allowed.", 400
        if mediatype not in ALLOWED_MEDIATYPES:
            return f"'{mediatype}' is not in {ALLOWED_MEDIATYPES}", 400
        return str(
            save_to_db_wrapper(
                {"artist": artist, "album": album_title, "mediatype": mediatype}
            )
        )
    else:
        return str(False)


if __name__ == "__main__":
    # Configure logging for VS Code terminal
    ignored_loggers = {}
    for ignored_logger in ignored_loggers:
        logging.getLogger(ignored_logger).setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    server = make_server("127.0.0.1", 2234, app)

    print("Server started!")

    server.serve_forever()
