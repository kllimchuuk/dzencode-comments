from rest_framework.views import APIView

from core.pagination import DefaultPagination

from .queries import get_comment_forest, get_root_comments
from .serializers import CommentSerializer


class CommentListView(APIView):
    def get(self, request):
        roots = get_root_comments(ordering=request.query_params.get("ordering"))
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(roots, request)
        forest = get_comment_forest(page)
        data = CommentSerializer(forest, many=True).data
        return paginator.get_paginated_response(data)
