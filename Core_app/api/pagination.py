from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    def get_page_number(self, request, paginator, view):
        page_number = super().get_page_number(request, paginator, view)
        return page_number - 1 if page_number > 0 else 0
