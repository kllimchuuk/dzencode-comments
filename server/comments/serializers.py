from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Comment


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


class CommentPreviewSerializer(serializers.Serializer):
    text = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_name",
            "email",
            "home_page",
            "text",
            "created_at",
            "replies",
        ]

    def get_replies(self, obj) -> list:
        return CommentSerializer(getattr(obj, "_children", []), many=True).data
