import typing
from urllib.parse import urlparse

from redis import Redis
from rq import Queue

from . import Crawler
from .components import URL, URLs
from .settings import MAX_NESTING_LIMIT, REDIS_DB, REDIS_HOST, REDIS_PORT

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
queue = Queue(connection=redis, result_ttl=0)


def filter_only_nested_to_specific_url(urls: URLs, specific_url: URL) -> URLs:
    filtered_urls = []
    for found_url in urls:
        parsed_url = urlparse(found_url)
        if (parsed_url.netloc + parsed_url.path).startswith(specific_url):
            filtered_urls.append(found_url)
    return filtered_urls


def crawl_url(
    key: str,
    status_key: str,
    url: URL,
    nesting_level: int,
    only_nesting_to_url: typing.Optional[URL] = None,
) -> None:
    pipeline = redis.pipeline(transaction=True)

    if nesting_level > MAX_NESTING_LIMIT:
        nesting_level = MAX_NESTING_LIMIT

    if not redis.sismember(key, url) and nesting_level > 0:
        crawler = Crawler()
        urls = crawler.crawl(url)

        if only_nesting_to_url:
            urls = filter_only_nested_to_specific_url(
                urls, only_nesting_to_url
            )

        pipeline.incrby(status_key, len(urls))
        queue.enqueue_many(
            [
                Queue.prepare_data(
                    crawl_url,
                    args=(
                        key,
                        status_key,
                        url,
                        nesting_level - 1,
                        only_nesting_to_url,
                    ),
                )
                for url in urls
            ],
            pipeline=pipeline,
        )

    pipeline.decr(status_key)
    pipeline.sadd(key, url)
    pipeline.execute()
