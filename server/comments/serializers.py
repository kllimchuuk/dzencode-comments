from rest_framework import serializers

from .models import Comment


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
