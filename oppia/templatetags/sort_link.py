from django import template
from django.utils.translation import ugettext

register = template.Library()


@register.inclusion_tag('oppia/includes/sort-link.html', takes_context=True)
def sort_link(context, attr_name, attr_title):
    ordering = context["page_ordering"] if ("page_ordering" in context) else None
    inverse_order = ordering is not None and ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]

    ajax_url = context["ajax_url"] if ("ajax_url" in context) else ""

    return {
        'request': context['request'],
        'title': ugettext(attr_title),
        'ajax_url': ajax_url,
        'orderby': attr_name,
        'ordered_ascending': (ordering == attr_name and not inverse_order),
        'ordered_descending': (ordering == attr_name and inverse_order)
    }
