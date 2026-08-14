from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError

from core.exceptions import ConflictException, ValidationException

from .models import User


class UserService:
    def register(self, *, username: str, email: str, password: str) -> User:
        self._ensure_username_available(username)
        self._ensure_email_available(email)
        self._validate_password(password)
        try:
            return User.objects.create_user(
                username=username, email=email, password=password
            )
        except IntegrityError:
            raise ConflictException(
                message="A user with these credentials already exists."
            )

    def _ensure_username_available(self, username: str) -> None:
        if User.objects.filter(username=username).exists():
            raise ConflictException(
                code="username_already_exists",
                message="A user with this username already exists.",
            )

    def _ensure_email_available(self, email: str) -> None:
        if User.objects.filter(email=email).exists():
            raise ConflictException(
                code="email_already_exists",
                message="A user with this email already exists.",
            )

    def _validate_password(self, password: str) -> None:
        try:
            validate_password(password)
        except DjangoValidationError as exc:
            raise ValidationException(
                message="Password does not meet requirements.",
                payload={"password": list(exc.messages)},
            )
