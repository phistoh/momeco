import hashlib
import logging

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


def save_str_to_file(filepath: str, content: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        logger.debug("Saved request to file: %s", filepath)


def copy_attributes(source, target):
    if not isinstance(source, dict):
        source = source.__dict__
    for key, value in source.items():
        if hasattr(target, key):
            setattr(target, key, value)


def get_dict_hash(d, *argv):
    """Method can receive additional arguments to append to the to-be-hashed string."""
    h = hashlib.new("sha256")
    object_as_str = [str(v or "") for v in d.values()]
    for arg in argv:
        object_as_str += str(arg)
    h.update("".join(object_as_str).encode("utf-8"))
    return h.hexdigest()


def remove_keys_from_dict(d: dict, keys_to_remove) -> dict:
    if isinstance(d, dict):
        return {
            key: remove_keys_from_dict(value, keys_to_remove)
            for key, value in d.items()
            if key not in keys_to_remove
        }
    elif isinstance(d, list):
        return [remove_keys_from_dict(item, keys_to_remove) for item in d]
    else:
        return d

def truncate_string(s: str, length: int) -> str:
    """Takes a string, truncates it to the given length, adding an ellipsis.

    Args:
        s (str): The string which will be shortened.
        length (int): The length of the shortened string including the length of the ellipsis.

    Returns:
        str: A truncated version of the string with given length (and ellipsis)
    """
    if not isinstance(s, str):
        logger.debug("'%s' is not a string.")
        return s
    ellipsis = "[…]"
    if len(s) > length:
        s = f"{s[:length-len(ellipsis)]}{ellipsis}"
    return s
