import hashlib
import typing
from urllib.parse import urlparse


def format_key(url: str, nesting_limit: int, only_nested_to_url: bool) -> str:
    key_hash = hashlib.md5(
        f"{nesting_limit} {url} {only_nested_to_url}".encode()
    )
    return key_hash.hexdigest()


def format_status_key(key: str) -> str:
    return f"{key}-status"


def queue_len_to_status(queue_len: typing.Optional[int]) -> str:
    if queue_len is None:
        return 'Not exist'
    if queue_len == 0:
        return 'Done'
    return 'Crawling'


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
