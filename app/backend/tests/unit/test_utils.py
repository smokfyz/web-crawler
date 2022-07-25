import pytest

from apps.crawler_api.utils import (
    format_key,
    format_status_key,
    queue_len_to_status,
    validate_url,
)


def test_format_key_return_same_hash_for_same_input():
    first_key = format_key('https://google.com/', 3, False)
    assert first_key == format_key('https://google.com/', 3, False)


def test_format_status_key_is_different():
    key = format_key('https://google.com/', 3, False)
    status_key = format_status_key(key)
    assert key != status_key


def test_queue_len_to_status_return_valid_status():
    assert queue_len_to_status(-50) == 'Crawling'
    assert queue_len_to_status(-1) == 'Crawling'
    assert queue_len_to_status(0) == 'Done'
    assert queue_len_to_status(1) == 'Crawling'
    assert queue_len_to_status(20) == 'Crawling'
    assert queue_len_to_status(None) == 'Not exist'


def test_url_validator():
    assert validate_url('http://google.com')
    assert validate_url('https://wiki.com')
    assert validate_url('htp://google.com')
    assert not validate_url('google.com')
    assert not validate_url('asdasd')
