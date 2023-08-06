from django import template
from ..service.get_favicon import get_favicons

register = template.Library()


@register.inclusion_tag('base_template/template_tags/favicon.html')
def favicon():
    favicons = get_favicons()
    return {'favicons': favicons}