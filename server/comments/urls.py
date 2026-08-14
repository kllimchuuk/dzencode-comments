from django.urls import path

from .views import CommentListCreateView, CommentPreviewView

urlpatterns = [
    path("", CommentListCreateView.as_view(), name="comment-list-create"),
    path("preview/", CommentPreviewView.as_view(), name="comment-preview"),
]
