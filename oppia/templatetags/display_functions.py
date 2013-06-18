# oppia/templatetags/display_functions.py
import json
from django import template

register = template.Library()

@register.filter(name='get_index')
def get_index(start,index):
    return start+index