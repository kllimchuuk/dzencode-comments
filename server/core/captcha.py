import base64
import random
import string
from io import BytesIO
from uuid import uuid4

from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont

CAPTCHA_LENGTH = 5
CAPTCHA_TTL = 300
CAPTCHA_ALPHABET = string.ascii_uppercase + string.digits


def render_captcha_image(text: str) -> str:
    image = Image.new("RGB", (160, 60), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=36)
    draw.text((15, 10), text, fill="black", font=font)
    for _ in range(6):
        draw.line(
            [
                random.randint(0, 160),
                random.randint(0, 60),
                random.randint(0, 160),
                random.randint(0, 60),
            ],
            fill="gray",
            width=1,
        )
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


class CaptchaService:
    def generate(self) -> dict:
        answer = "".join(random.choices(CAPTCHA_ALPHABET, k=CAPTCHA_LENGTH))
        token = uuid4().hex
        cache.set(self._key(token), answer, timeout=CAPTCHA_TTL)
        return {"token": token, "image": render_captcha_image(answer)}

    def validate(self, token: str, answer: str) -> bool:
        stored = cache.get(self._key(token))
        if stored is None:
            return False
        cache.delete(self._key(token))
        return stored.casefold() == answer.casefold()

    def _key(self, token: str) -> str:
        return f"captcha:{token}"
