from core.exceptions import NotFoundException, ValidationException


class InvalidHTMLException(ValidationException):
    def __init__(
        self,
        message: str = "Comment text is not valid XHTML.",
        payload: dict | None = None,
    ) -> None:
        super().__init__(message=message, payload=payload, code="invalid_html")


class ParentNotFoundException(NotFoundException):
    def __init__(
        self,
        message: str = "Parent comment not found.",
        payload: dict | None = None,
    ) -> None:
        super().__init__(message=message, payload=payload, code="parent_not_found")


class InvalidCaptchaException(ValidationException):
    def __init__(
        self,
        message: str = "Invalid or expired captcha.",
        payload: dict | None = None,
    ) -> None:
        super().__init__(message=message, payload=payload, code="invalid_captcha")


class InvalidAttachmentException(ValidationException):
    def __init__(
        self,
        message: str = "Attachment must be a JPG/PNG/GIF image (<=5MB) or a .txt file (<=100KB).",
        payload: dict | None = None,
    ) -> None:
        super().__init__(message=message, payload=payload, code="invalid_attachment")
