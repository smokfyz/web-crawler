import pytest


@pytest.fixture
def html_page():
    return '<body><a href="/hello_world"></a><div><a href="https://wiki.com" /></div></body>'
