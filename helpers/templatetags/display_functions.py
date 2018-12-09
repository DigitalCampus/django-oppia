# oppia/templatetags/display_functions.py
import hashlib
import json
import math
import urllib

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='get_index')
def get_index(start, index):
    return start + index


@register.filter(name='secs_to_duration')
def secs_to_duration(secs):
    if secs == 0:
        return "-"

    if secs < 60:
        return "< 1 min"

    if secs < 120:
        return "1 min"

    return str(int(math.floor(secs / 60))) + " mins"

@register.filter(name='title_lang')
@stringfilter
def title_lang(title, lang):
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


@register.filter(name='gravatar')
def gravatar(user, size):
    gravatar_url = "https://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id': hashlib.md5(user.email).hexdigest(),
        'size': str(size)
    })
    return mark_safe(
        '<img src="{0}" alt="gravatar for {1}" class="gravatar" width="{2}" height="{2}"/>'.format(gravatar_url, user, size)
        )
