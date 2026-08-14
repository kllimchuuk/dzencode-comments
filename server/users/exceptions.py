from rest_framework import status

from core.exceptions import AppException


class InvalidTokenException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message="Invalid or missing refresh token.", payload=None):
        super().__init__(code="invalid_token", message=message, payload=payload)
