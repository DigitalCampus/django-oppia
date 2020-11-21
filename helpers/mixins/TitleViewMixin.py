class TitleViewMixin(object):
    """
    A mixin to add the defined title to the context
    """

    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleViewMixin, self).get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.view_title

        return context
