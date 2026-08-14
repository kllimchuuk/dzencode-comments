from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: list) -> Response:
        return Response(
            {
                "page": self.page.number,
                "size": self.get_page_size(self.request),
                "total_pages": self.page.paginator.num_pages,
                "total": self.page.paginator.count,
                "results": data,
            }
        )
