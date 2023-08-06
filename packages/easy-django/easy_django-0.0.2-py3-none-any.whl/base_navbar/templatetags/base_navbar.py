from django import template
from ..service.get_navbar import get_navbar

register = template.Library()


@register.inclusion_tag('base_navbar/base_navbar.html')
def base_navbar():
    navbar = get_navbar()
    context = {
        'navbar': navbar
    }
    return context