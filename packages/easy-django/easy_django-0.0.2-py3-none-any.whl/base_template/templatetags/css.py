from django import template
from ..service.get_css import get_csss

register = template.Library()


@register.inclusion_tag('base_template/template_tags/css.html')
def csss():
    csss = get_csss()
    return {"csss": csss}