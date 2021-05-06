from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class PaginationCategoryDetail(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        print(data)
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('current', self.page.number),
            ('results', data)
        ]))

