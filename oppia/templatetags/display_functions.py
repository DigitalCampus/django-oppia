# oppia/templatetags/display_functions.py
import json
import math
from django import template

register = template.Library()

@register.filter(name='get_index')
def get_index(start,index):
    return start+index

@register.filter(name='secs_to_duration')
def secs_to_duration(secs):
    minutes = int(math.floor(secs/60))
    seconds = int(secs - (minutes*60))
    return str(minutes)+'\''+str(seconds)+'"'