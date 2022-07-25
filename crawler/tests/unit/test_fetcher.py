import pytest

from crawler.components.fetcher import URLFetcher, requests


def test_extract_page_request(mocker):
    mocker.patch('crawler.components.fetcher.requests.get')
    fetcher = URLFetcher()
    fetcher.get_page_content('https://google.com/')
    requests.get.assert_called_once_with('https://google.com/', timeout=5)
