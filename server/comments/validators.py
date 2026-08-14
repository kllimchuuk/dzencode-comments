from PIL import Image, UnidentifiedImageError

from .exceptions import InvalidAttachmentException
from .models import Attachment

ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "GIF"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_TEXT_SIZE = 100 * 1024


class FileTypeStrategy:
    kind: str

    def matches(self, file) -> bool:
        raise NotImplementedError


class ImageFile(FileTypeStrategy):
    kind = Attachment.Kind.IMAGE

    def matches(self, file) -> bool:
        return (
            self._within_limit(file)
            and self._is_intact(file)
            and self._format(file) in ALLOWED_IMAGE_FORMATS
        )

    def _within_limit(self, file) -> bool:
        return file.size <= MAX_IMAGE_SIZE

    def _is_intact(self, file) -> bool:
        file.seek(0)
        try:
            Image.open(file).verify()
        except (UnidentifiedImageError, OSError, SyntaxError):
            return False
        finally:
            file.seek(0)
        return True

    def _format(self, file) -> str | None:
        file.seek(0)
        try:
            image = Image.open(file)
        except (UnidentifiedImageError, OSError):
            return None
        finally:
            file.seek(0)
        return image.format


class TextFile(FileTypeStrategy):
    kind = Attachment.Kind.TEXT

    def matches(self, file) -> bool:
        return (
            self._has_txt_extension(file)
            and self._within_limit(file)
            and self._is_utf8(file)
        )

    def _has_txt_extension(self, file) -> bool:
        return file.name.lower().endswith(".txt")

    def _within_limit(self, file) -> bool:
        return file.size <= MAX_TEXT_SIZE

    def _is_utf8(self, file) -> bool:
        file.seek(0)
        try:
            file.read().decode("utf-8")
        except UnicodeDecodeError:
            return False
        finally:
            file.seek(0)
        return True


class AttachmentValidator:
    _strategies = (ImageFile(), TextFile())

    def validate(self, file) -> str:
        for strategy in self._strategies:
            if strategy.matches(file):
                return strategy.kind
        raise InvalidAttachmentException()
