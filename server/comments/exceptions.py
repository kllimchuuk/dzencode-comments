from rest_framework import status

from core.exceptions import AppException


class InvalidHTMLException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, message="Comment text is not valid XHTML.", payload=None):
        super().__init__(code="invalid_html", message=message, payload=payload)


class ParentNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message="Parent comment not found.", payload=None):
        super().__init__(code="parent_not_found", message=message, payload=payload)


class InvalidCaptchaException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message="Invalid or expired captcha.", payload=None):
        super().__init__(code="invalid_captcha", message=message, payload=payload)
