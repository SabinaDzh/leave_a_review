from rest_framework.pagination import PageNumberPagination


PAGE_SIZE = 5


class Pagination(PageNumberPagination):
    page_size = PAGE_SIZE
