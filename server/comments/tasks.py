import logging

from celery import shared_task
from PIL import Image

from .models import Attachment

logger = logging.getLogger(__name__)

MAX_IMAGE_DIMENSIONS = (320, 240)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def process_image(self, attachment_id: int) -> None:
    attachment = Attachment.objects.filter(pk=attachment_id).first()
    if attachment is None:
        logger.warning("process_image: attachment %s not found", attachment_id)
        return
    try:
        _resize(attachment)
    except OSError as exc:
        logger.warning("process_image: resize failed for %s: %s", attachment_id, exc)
        raise self.retry(exc=exc)


def _resize(attachment: Attachment) -> None:
    image = Image.open(attachment.file)
    image_format = image.format
    image.thumbnail(MAX_IMAGE_DIMENSIONS)
    image.save(attachment.file.path, format=image_format)
