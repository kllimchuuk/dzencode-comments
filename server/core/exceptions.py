from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str
    message: str
    payload: dict

    def __init__(self, code: str, message: str, payload: dict | None = None) -> None:
        self.code = code
        self.message = message
        self.payload = payload or {}
        super().__init__(message)


class ValidationException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(
        self,
        message: str = "Validation error",
        payload: dict | None = None,
        code: str = "validation_error",
    ) -> None:
        super().__init__(code=code, message=message, payload=payload)


class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Unauthorized",
        payload: dict | None = None,
    ) -> None:
        super().__init__(code="unauthorized", message=message, payload=payload)


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(
        self,
        message: str = "Forbidden",
        payload: dict | None = None,
    ) -> None:
        super().__init__(code="forbidden", message=message, payload=payload)


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        message: str = "Entity not found",
        payload: dict | None = None,
        code: str = "not_found",
    ) -> None:
        super().__init__(code=code, message=message, payload=payload)


class ConflictException(AppException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(
        self,
        code: str = "conflict",
        message: str = "Resource already exists.",
        payload: dict | None = None,
    ) -> None:
        super().__init__(code=code, message=message, payload=payload)


class TooManyRequestsException(AppException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __init__(
        self,
        message: str = "Too many requests",
        payload: dict | None = None,
    ) -> None:
        super().__init__(code="too_many_requests", message=message, payload=payload)


def drf_exception_handler(exc, context):
    if isinstance(exc, AppException):
        return Response(
            {"code": exc.code, "message": exc.message, "payload": exc.payload},
            status=exc.status_code,
        )
    return exception_handler(exc, context)
