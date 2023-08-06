from django import template
from ..service.get_head_meta import get_head_meta

register = template.Library()


@register.inclusion_tag('base_template/template_tags/head_meta.html')
def head_meta():
    head_meta = get_head_meta()
    return {"head_meta": head_meta}