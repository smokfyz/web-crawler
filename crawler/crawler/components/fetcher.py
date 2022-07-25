import logging
import typing

import requests

from .types import URL, HTMLPage

log = logging.getLogger(__name__)


class URLFetcher:
    @staticmethod
    def get_page_content(url: URL) -> typing.Optional[HTMLPage]:
        try:
            return requests.get(url, timeout=5).text
        except Exception as err:
            logging.warning(f"Cannot fetch URL: {url}. Exception: {err}.")
            return None
