from celery import shared_task
from PIL import Image

from .models import Attachment

MAX_IMAGE_DIMENSIONS = (320, 240)


@shared_task
def process_image(attachment_id: int) -> None:
    attachment = Attachment.objects.get(pk=attachment_id)
    image = Image.open(attachment.file)
    image.thumbnail(MAX_IMAGE_DIMENSIONS)
    image.save(attachment.file.path)
