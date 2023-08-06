from django.conf import settings
import re
import itertools
from django.http import Http404, HttpResponseBadRequest

from .utils import get_client_ip
from .models import DigRule


class DjangoIpGuardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if settings.DIG_ENABLED:
            blocker_url_list = None
            blocker_ip_list = None
            allower_url_list = None
            allower_ip_list = None
            if settings.DIG_STORAGE == "db" or not settings.DIG_STORAGE:
                dig_rule = DigRule.objects.first()
                if dig_rule:
                    blocker_url_list = dig_rule.blocker_url_patterns.split() if dig_rule.blocker_url_patterns else None
                    blocker_ip_list = dig_rule.blocker_ip_patterns.split() if dig_rule.blocker_ip_patterns else None
                    allower_url_list = dig_rule.allower_url_patterns.split() if dig_rule.allower_url_patterns else None
                    allower_ip_list = dig_rule.allower_ip_patterns.split() if dig_rule.allower_ip_patterns else None
                
            elif settings.DIG_STORAGE == "env":
                blocker_url_list = settings.BLOCKER_URL_PATTERNS.split(",") if settings.BLOCKER_URL_PATTERNS else None
                blocker_ip_list = settings.BLOCKER_IP_PATTERNS.split(",") if settings.BLOCKER_IP_PATTERNS else None
                allower_url_list = settings.ALLOWER_URL_PATTERNS.split(",") if settings.ALLOWER_URL_PATTERNS else None
                allower_ip_list = settings.ALLOWER_IP_PATTERNS.split(",") if settings.ALLOWER_IP_PATTERNS else None

            client_ip = get_client_ip(request)
            requested_url = request.path

            if blocker_url_list and blocker_ip_list and client_ip:
                if re.search("|".join(blocker_url_list), requested_url) and re.search("|".join(blocker_ip_list), client_ip):
                    return HttpResponseBadRequest(status=400, content="Bad Request")

            if allower_url_list and allower_ip_list and client_ip:
                if re.search("|".join(allower_url_list), requested_url) and not re.search("|".join(allower_ip_list), client_ip):
                    return HttpResponseBadRequest(status=400, content="Bad Request")
