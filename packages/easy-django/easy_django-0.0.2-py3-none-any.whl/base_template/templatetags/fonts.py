from django import template
from ..service.get_fonts import get_fonts


register = template.Library()


@register.inclusion_tag('base_template/template_tags/fonts.html')
def fonts():
    fonts = get_fonts()
    return {'fonts': fonts}