from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Attachment, Comment


class CommentCreateSerializer(serializers.Serializer):
    parent = serializers.IntegerField(required=False, allow_null=True)
    user_name = serializers.CharField(
        max_length=60, validators=[RegexValidator(r"^[A-Za-z0-9]+$")]
    )
    email = serializers.EmailField()
    home_page = serializers.URLField(required=False, allow_blank=True)
    text = serializers.CharField()
    captcha_token = serializers.CharField()
    captcha_answer = serializers.CharField()
    file = serializers.FileField(required=False, allow_null=True)


class CommentPreviewSerializer(serializers.Serializer):
    text = serializers.CharField()


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="file.url", read_only=True)

    class Meta:
        model = Attachment
        fields = ["url", "kind"]


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "user_name",
            "email",
            "home_page",
            "text",
            "created_at",
            "attachment",
            "replies",
        ]

    def get_replies(self, obj) -> list:
        return CommentSerializer(getattr(obj, "_children", []), many=True).data

    def get_attachment(self, obj) -> dict | None:
        attachment = getattr(obj, "attachment", None)
        return AttachmentSerializer(attachment).data if attachment else None
