from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.captcha import CaptchaService
from core.pagination import DefaultPagination
from core.throttling import WriteScopedRateThrottle

from .queries import get_comment_forest, get_root_comments
from .serializers import (
    CommentCreateSerializer,
    CommentPreviewSerializer,
    CommentSerializer,
)
from .services import CommentService


class CaptchaView(APIView):
    throttle_scope = "captcha"

    def get(self, request):
        return Response(CaptchaService().generate())


class CommentPreviewView(APIView):
    throttle_scope = "preview"

    def post(self, request):
        serializer = CommentPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        html = CommentService().preview(serializer.validated_data["text"])
        return Response({"text": html})


class CommentListCreateView(APIView):
    throttle_classes = [WriteScopedRateThrottle]
    throttle_scope = "comment_create"

    def get(self, request):
        roots = get_root_comments(ordering=request.query_params.get("ordering"))
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(roots, request)
        forest = get_comment_forest(page)
        data = CommentSerializer(forest, many=True).data
        return paginator.get_paginated_response(data)

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = CommentService().create(
            data=serializer.validated_data,
            user=request.user,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
        comment._children = []
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
