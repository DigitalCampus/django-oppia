from django.views import View


class TitleViewMixin(View):
    """
    A mixin to add the defined title to the context
    """

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title

        return context
