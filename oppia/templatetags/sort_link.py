import urllib

from django import template
from django.utils.translation import ugettext

register = template.Library()

@register.inclusion_tag('oppia/includes/sort-link.html', takes_context=True)
def sort_link(context, attr_name, attr_title):
    ordering = context["page_ordering"]
    inverse_order = ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]

    return {
        'title': ugettext(attr_title),
        'orderby': attr_name,
        'ordered_ascending': (ordering == attr_name and not inverse_order),
        'ordered_descending': (ordering == attr_name and inverse_order)
    }