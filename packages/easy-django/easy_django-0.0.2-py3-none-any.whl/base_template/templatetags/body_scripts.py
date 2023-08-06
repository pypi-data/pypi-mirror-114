from django import template
from ..service.get_body_scripts import get_body_scripts

register = template.Library()


@register.inclusion_tag('base_template/template_tags/body_scripts.html')
def body_scripts():
    body_scripts = get_body_scripts()
    return {"body_scripts": body_scripts}