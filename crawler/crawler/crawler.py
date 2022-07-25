import logging

from .components import URL, URLExtractor, URLFetcher, URLs

log = logging.getLogger(__name__)


class Crawler:
    def __init__(self) -> None:
        self.extractor = URLExtractor()
        self.fetcher = URLFetcher()

    def crawl(self, url: URL) -> URLs:
        html_page = self.fetcher.get_page_content(url)
        if html_page is None:
            return []
        return self.extractor.extract_urls(url, html_page)
