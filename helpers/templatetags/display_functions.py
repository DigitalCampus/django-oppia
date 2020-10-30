# oppia/templatetags/display_functions.py
import hashlib
import json
import math
import re
import urllib

import itertools
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
            for temp_lang in titles:
                return titles[temp_lang]
    except json.JSONDecodeError:
        pass

    # Patch for wrong strings saved as python dicts
    dict_regex = "u\'([a-zA-Z_-]+)\': *u\'([A-Za-z ?!%&#$().0-9@,\\\n_:-]+)\'"
    langs = re.search(dict_regex, title)
    if langs:
        return langs.group(2)

    return title


@register.filter(name='gravatar')
def gravatar(user, size):
    gravatar_url = "https://www.gravatar.com/avatar.php?"
    gravatar_id = hashlib.md5(str(user.email).encode('utf-8')).hexdigest()
    gravatar_url += urllib.parse.urlencode({
        'gravatar_id': gravatar_id,
        'size': str(size)
    })
    return mark_safe(
        '<img src="{0}" alt="gravatar for {1}" \
        class="gravatar" width="{2}" height="{2}"/>'.format(gravatar_url,
                                                            user,
                                                            size)
        )


@register.filter(name='lookup')
def lookup(value, key):
    return value.get(key)


@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break


@register.filter
def split_half(list):
    """
    Breaks a list up into a list of two lists of half size
    """
    half = len(list) // 2
    return [list[:half], list[half:]]
