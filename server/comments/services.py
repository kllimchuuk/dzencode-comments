import nh3
from lxml import etree

from core.captcha import CaptchaService

from .exceptions import (
    InvalidCaptchaException,
    InvalidHTMLException,
    ParentNotFoundException,
)
from .models import Comment

ALLOWED_TAGS = {"a", "code", "i", "strong"}
ALLOWED_ATTRIBUTES = {"a": {"href", "title"}}


class CommentService:
    def create(self, *, data: dict, user, ip_address, user_agent: str) -> Comment:
        self._validate_captcha(data["captcha_token"], data["captcha_answer"])
        self._validate_xhtml(data["text"])
        parent = self._resolve_parent(data.get("parent"))
        return Comment.objects.create(
            parent=parent,
            user=user if user.is_authenticated else None,
            user_name=data["user_name"],
            email=data["email"],
            home_page=data.get("home_page", ""),
            text=self._sanitize(data["text"]),
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def preview(self, text: str) -> str:
        self._validate_xhtml(text)
        return self._sanitize(text)

    def _validate_captcha(self, token: str, answer: str) -> None:
        if not CaptchaService().validate(token, answer):
            raise InvalidCaptchaException()

    def _validate_xhtml(self, text: str) -> None:
        try:
            etree.fromstring(f"<div>{text}</div>")
        except etree.XMLSyntaxError:
            raise InvalidHTMLException()

    def _sanitize(self, text: str) -> str:
        return nh3.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

    def _resolve_parent(self, parent_id: int | None) -> Comment | None:
        if parent_id is None:
            return None
        try:
            return Comment.objects.get(pk=parent_id)
        except Comment.DoesNotExist:
            raise ParentNotFoundException()
