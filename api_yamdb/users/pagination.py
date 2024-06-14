from rest_framework.pagination import PageNumberPagination


PAGE_SIZE = 5


class UsersPagination(PageNumberPagination):
    page_size = PAGE_SIZE
