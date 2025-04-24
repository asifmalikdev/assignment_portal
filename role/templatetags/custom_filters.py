# role/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    """Adds a class to an HTML element's class attribute."""
    if isinstance(value, str):
        return value + ' ' + class_name
    return value
