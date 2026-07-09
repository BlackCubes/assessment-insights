from collections.abc import Sequence
from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that extends the default PageNumberPagination provided by Django REST Framework.
    This class allows for customization of the pagination behavior, including the ability to specify a custom page size query parameter and a maximum page size limit. It also provides a method to generate a paginated response with additional metadata about the pagination state.

    Attributes
    ----------
        page_size_query_param (str): The query parameter name for specifying the page size. Default is "pageSize".
        max_page_size (int): The maximum number of items allowed per page. Default is 100.

    Methods
    -------
        get_paginated_response(data: Sequence[Any]) -> Response:
            Generates a paginated response containing the paginated data and metadata about the pagination state, including the total count of items, current page number, page size, number of items on the current page, total number of pages, and links to the next and previous pages.
    """

    page_size_query_param = "pageSize"
    max_page_size = 100

    def get_paginated_response(self, data: Sequence[Any]) -> Response:
        return Response(
            {
                "results": data,
                "metaData": {
                    "count": self.page.paginator.count,
                    "page": self.page.number,
                    "pageSize": self.get_page_size(self.request),
                    "itemsOnPage": len(data),
                    "totalPages": self.page.paginator.num_pages,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )
