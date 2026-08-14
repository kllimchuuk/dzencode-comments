import nh3
from django.db import transaction
from lxml import etree
from PIL import Image, UnidentifiedImageError

from core.captcha import CaptchaService

from .exceptions import (
    InvalidAttachmentException,
    InvalidCaptchaException,
    InvalidHTMLException,
    ParentNotFoundException,
)
from .models import Attachment, Comment

ALLOWED_TAGS = {"a", "code", "i", "strong"}
ALLOWED_ATTRIBUTES = {"a": {"href", "title"}}
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "GIF"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_TEXT_SIZE = 100 * 1024


class CommentService:
    def create(self, *, data: dict, user, ip_address, user_agent: str) -> Comment:
        self._validate_captcha(data["captcha_token"], data["captcha_answer"])
        self._validate_xhtml(data["text"])
        parent = self._resolve_parent(data.get("parent"))
        file = data.get("file")
        kind = self._validate_file(file) if file else None
        with transaction.atomic():
            comment = Comment.objects.create(
                parent=parent,
                user=user if user.is_authenticated else None,
                user_name=data["user_name"],
                email=data["email"],
                home_page=data.get("home_page", ""),
                text=self._sanitize(data["text"]),
                ip_address=ip_address,
                user_agent=user_agent,
            )
            if file:
                Attachment.objects.create(comment=comment, file=file, kind=kind)
        return comment

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

    def _validate_file(self, file) -> str:
        checks = (
            (Attachment.Kind.IMAGE, self._is_image),
            (Attachment.Kind.TEXT, self._is_text),
        )
        for kind, is_valid in checks:
            if is_valid(file):
                return kind
        raise InvalidAttachmentException()

    def _is_image(self, file) -> bool:
        return (
            self._within_limit(file, MAX_IMAGE_SIZE)
            and self._image_is_intact(file)
            and self._image_format(file) in ALLOWED_IMAGE_FORMATS
        )

    def _is_text(self, file) -> bool:
        return (
            self._has_txt_extension(file)
            and self._within_limit(file, MAX_TEXT_SIZE)
            and self._is_utf8(file)
        )

    def _within_limit(self, file, limit: int) -> bool:
        return file.size <= limit

    def _has_txt_extension(self, file) -> bool:
        return file.name.lower().endswith(".txt")

    def _image_is_intact(self, file) -> bool:
        file.seek(0)
        try:
            Image.open(file).verify()
        except (UnidentifiedImageError, OSError, SyntaxError):
            return False
        finally:
            file.seek(0)
        return True

    def _image_format(self, file) -> str | None:
        file.seek(0)
        try:
            image = Image.open(file)
        except (UnidentifiedImageError, OSError):
            return None
        finally:
            file.seek(0)
        return image.format

    def _is_utf8(self, file) -> bool:
        file.seek(0)
        try:
            file.read().decode("utf-8")
        except UnicodeDecodeError:
            return False
        finally:
            file.seek(0)
        return True
