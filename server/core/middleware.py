class RealClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            request.META["REMOTE_ADDR"] = forwarded.split(",")[0].strip()
        return self.get_response(request)
