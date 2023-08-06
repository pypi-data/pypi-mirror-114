from django import template
from ..service.get_base_template_cache_time import get_base_template_cache_time_by_part

register = template.Library()


@register.inclusion_tag('base_template/cached_head.html')
def cached_head():
    cached_head_time = get_base_template_cache_time_by_part('HEAD')
    return {"cached_head_time": cached_head_time}