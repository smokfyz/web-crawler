from http import HTTPStatus
from urllib.parse import urlparse

import django_rq
import redis
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View

from .utils import (
    format_key,
    format_status_key,
    queue_len_to_status,
    validate_url,
)


redis_connection = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


class Status(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        job_hash = request.GET.get('hash')

        if job_hash is None:
            return JsonResponse(
                {
                    'status': 'success',
                },
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        status_key = format_status_key(job_hash)

        number_of_urls = redis_connection.scard(job_hash)
        queue_len_str = redis_connection.get(status_key)
        queue_len = int(queue_len_str) if queue_len_str is not None else None

        return JsonResponse(
            {
                'status': 'success',
                'result': {
                    'number_of_urls': number_of_urls,
                    'job_status': queue_len_to_status(queue_len),
                },
            },
            status=HTTPStatus.OK,
        )


class Tasks(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        job_hash = request.GET.get('hash')

        if job_hash is None:
            return JsonResponse(
                {
                    'status': 'error',
                },
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        urls = redis_connection.smembers(job_hash)

        return JsonResponse(
            {'status': 'success', 'result': {'urls': list(urls)}},
            status=HTTPStatus.OK,
        )

    def post(self, request: HttpRequest) -> JsonResponse:
        url = request.POST.get('url')
        nesting_limit = int(request.POST.get('nesting_limit', 2))
        only_nested_to_url = request.POST.get('only_nested_to_url', False)

        if url is None or not validate_url(url):
            return JsonResponse(
                {
                    'status': 'error',
                },
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        queue = django_rq.get_queue('default', result_ttl=0)

        job_hash = format_key(url, nesting_limit, only_nested_to_url)
        status_key = format_status_key(job_hash)

        redis_connection.incr(status_key)

        parsed_url = urlparse(url)
        queue.enqueue(
            'crawler.worker.crawl_url',
            args=(
                job_hash,
                status_key,
                url,
                nesting_limit,
                (parsed_url.netloc + parsed_url.path)
                if only_nested_to_url
                else None,
            ),
        )

        return JsonResponse(
            {'status': 'success', 'result': {'hash': job_hash}},
            status=HTTPStatus.OK,
        )
