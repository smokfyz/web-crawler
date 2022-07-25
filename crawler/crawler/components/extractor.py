import logging
import typing
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from .types import URL, HTMLPage, URLs

log = logging.getLogger(__name__)


class ATagsParser(HTMLParser):
    def __init__(self) -> None:
        self.hrefs: typing.List[typing.Optional[str]] = []
        super().__init__()

    def handle_starttag(
        self,
        tag: str,
        attrs: typing.List[typing.Tuple[str, typing.Optional[str]]],
    ) -> None:
        if tag == "a":
            for attr in attrs:
                if attr[0] != "href":
                    continue
                self.hrefs.append(attr[1])


class URLExtractor:
    @staticmethod
    def _is_valid(url: str) -> bool:
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def _process_hrefs(
        self, processed_url: URL, hrefs: typing.List[typing.Optional[str]]
    ) -> URLs:
        found_urls = set()

        for href in hrefs:
            if href is None:
                continue

            href = urljoin(processed_url, href)
            parsed_href = urlparse(href)
            href = (
                parsed_href.scheme
                + "://"
                + parsed_href.netloc
                + parsed_href.path
            )

            if not self._is_valid(href) or href in found_urls:
                continue

            found_urls.add(href)

        return list(found_urls)

    def extract_urls(self, processed_url: URL, html_page: HTMLPage) -> URLs:
        parser = ATagsParser()
        parser.feed(html_page)
        hrefs = parser.hrefs
        return self._process_hrefs(processed_url, hrefs)
