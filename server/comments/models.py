from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from tree_queries.fields import TreeNodeForeignKey
from tree_queries.query import TreeQuerySet

from core.models import TimeStampedModel


class CommentQuerySet(TreeQuerySet):
    def roots(self):
        return self.filter(parent__isnull=True)


class Comment(TimeStampedModel):
    parent = TreeNodeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="comments",
    )
    user_name = models.CharField(
        max_length=60,
        validators=[RegexValidator(r"^[A-Za-z0-9]+$")],
    )
    email = models.EmailField()
    home_page = models.URLField(blank=True)
    text = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    objects = CommentQuerySet.as_manager()

    class Meta:
        indexes = [models.Index(fields=["-created_at"])]

    def __str__(self):
        return f"{self.user_name}: {self.text[:50]}"


class Attachment(TimeStampedModel):
    class Kind(models.TextChoices):
        IMAGE = "image"
        TEXT = "text"

    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachment",
    )
    file = models.FileField(upload_to="attachments/")
    kind = models.CharField(max_length=5, choices=Kind.choices)

    def __str__(self):
        return f"{self.kind}: {self.file.name}"
