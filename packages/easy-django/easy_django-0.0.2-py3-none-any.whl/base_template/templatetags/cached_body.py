from django import template
from ..service.get_base_template_cache_time import get_base_template_cache_time_by_part

register = template.Library()


@register.inclusion_tag('base_template/cached_body.html')
def cached_body():
    cached_body_time = get_base_template_cache_time_by_part('BODY')
    return {"cached_body_time": cached_body_time}