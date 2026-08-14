from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView


class WriteScopedRateThrottle(ScopedRateThrottle):
    def allow_request(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return super().allow_request(request, view)
