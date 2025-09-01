from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)


class PageNumberProductPagination(PageNumberPagination):
    page_size = 3
    page_query_param = "page_size"
    max_page_size = 50


class LimitOffsetProductPagination(LimitOffsetPagination):
    default_limit = 4
    # limit_query_param = "yeti_ota"
    # offset_query_param = "yeta_dekhi"


class CursorProductPaginationWithOrdering(CursorPagination):
    ordering = "id"
