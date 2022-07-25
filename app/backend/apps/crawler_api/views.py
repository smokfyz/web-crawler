import django_rq
from redis import Redis

from django.http import JsonResponse
from http import HTTPStatus


redis_connection = Redis(host='localhost', port=6379, db=0)


def format_key_for_redis(url: str, nesting_limit: int = 3) -> str:
    return f"{nesting_limit} {url}"


def tasks(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        nesting_limit = request.GET.get('nesting_limit')

        urls = redis_connection.smembers(
            format_key_for_redis(url, nesting_limit)
        )

        return JsonResponse({
            'status': 'success',
            'result': urls
        }, status=HTTPStatus.OK)

    if request.method == 'POST':
        url = request.POST.get('url')
        nesting_limit = request.POST.get('nesting_limit')

        queue = django_rq.get_queue('default', default_timeout=60)
        queue.enqueue(
            'crawler.worker.crawl_url',
            args=(
                format_key_for_redis(url, nesting_limit),
                url,
                3
            )
        )

        return JsonResponse({
            'status': 'success'
        }, status=HTTPStatus.OK)
