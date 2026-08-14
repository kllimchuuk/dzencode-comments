from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "comments"

    def ready(self):
        from django.db.models.signals import post_save

        from .models import Comment
        from .signals import broadcast_comment

        post_save.connect(broadcast_comment, sender=Comment)
