from django import template

register = template.Library()


@register.filter
def obj_type(obj):
    return type(obj).__name__







