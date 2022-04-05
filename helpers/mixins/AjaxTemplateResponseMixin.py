from django.views.generic.base import TemplateResponseMixin
from helpers.ajax import is_ajax

class AjaxTemplateResponseMixin(TemplateResponseMixin):
    """
    A mixin that can be used to render a different templates based in the
    kind of request (Ajax or not).
    """

    ajax_template_name = None

    def render_to_response(self, context, **response_kwargs):
        """
        If the request is Ajax, it adds the needed headers to the response
        """

        response = super(AjaxTemplateResponseMixin, self) \
            .render_to_response(context, **response_kwargs)
        if is_ajax(self.request):
            response['Cache-Control'] = 'no-cache'
            response['Vary'] = 'Accept'
        return response

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must
        return a list. May not be called if render_to_response is overridden.
        """

        template_names = None
        if is_ajax(self.request) and self.ajax_template_name is not None:
            template_names = [self.ajax_template_name, self.template_name]

        if template_names is None:
            template_names = super(AjaxTemplateResponseMixin, self) \
                .get_template_names()

        return template_names
