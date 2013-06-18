# oppia/templatetags/display_functions.py
import json
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.filter(name='title_lang')
@stringfilter
def title_lang(title,lang):
    try:
        titles = json.loads(title)
        if lang in titles:
            return titles[lang]
        else:
            for l in titles:
                return titles[l]
    except:
        pass
    return title