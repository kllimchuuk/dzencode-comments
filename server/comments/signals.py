from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from .consumers import GROUP
from .models import Comment
from .serializers import CommentSerializer


def broadcast_comment(sender, instance, created, **kwargs):
    if not created:
        return
    transaction.on_commit(lambda: _broadcast(instance.pk))


def _broadcast(comment_id):
    comment = Comment.objects.select_related("attachment").get(pk=comment_id)
    payload = CommentSerializer(comment).data
    async_to_sync(get_channel_layer().group_send)(
        GROUP, {"type": "comment_created", "comment": payload}
    )
