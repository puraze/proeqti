# products/templatetags/i18n_extras.py

from django import template
from django.utils.translation import get_language_info, get_language

register = template.Library()

@register.simple_tag
def get_current_language_name():
    lang_code = get_language()
    lang_info = get_language_info(lang_code)
    return lang_info['name_local']