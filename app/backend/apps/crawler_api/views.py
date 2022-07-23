import logging
import time

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from http import HTTPStatus


log = logging.getLogger(__name__)


@require_http_methods(["POST"])
def crawl_page(request):
    log.info(f"# {request.POST.get('url')}")
    time.sleep(3)
    return JsonResponse({
        'urls': ['http://test.com', 'http://test1.com', 'http://test2.com']
    }, status=HTTPStatus.OK)
