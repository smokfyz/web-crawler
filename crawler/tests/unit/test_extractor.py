import pytest

from crawler.components.extractor import URLExtractor


def test_url_extractor_return_expected_urls(html_page):
    url_extractor = URLExtractor()

    urls = url_extractor.extract_urls('https://google.com', html_page)
    assert len(set(urls) ^ {'https://google.com/hello_world', 'https://wiki.com'}) == 0
