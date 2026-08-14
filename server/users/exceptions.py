from core.exceptions import ValidationException


class InvalidTokenException(ValidationException):
    def __init__(
        self,
        message: str = "Invalid or missing refresh token.",
        payload: dict | None = None,
    ) -> None:
        super().__init__(message=message, payload=payload, code="invalid_token")
