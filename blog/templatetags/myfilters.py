from django import template

register = template.Library()


@register.filter(name='type')
def obj_type(obj):
    return type(obj).__name__


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)
