from django import template
from ..service.get_head_link import get_head_links

register = template.Library()


@register.inclusion_tag('base_template/template_tags/head_links.html')
def head_links():
    head_links = get_head_links()
    return {"head_links": head_links}