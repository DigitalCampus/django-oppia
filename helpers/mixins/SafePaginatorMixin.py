from django.core.paginator import Paginator, EmptyPage, InvalidPage

class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except (EmptyPage, InvalidPage):
            if number > 1:
                return self.num_pages
            else:
                raise


class SafePaginatorMixin(object):

    paginator_class = SafePaginator

    def paginate_queryset(self, queryset, page_size):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            self.kwargs[page_kwarg] = "last"

        return super(SafePaginatorMixin, self).paginate_queryset(queryset, page_size)