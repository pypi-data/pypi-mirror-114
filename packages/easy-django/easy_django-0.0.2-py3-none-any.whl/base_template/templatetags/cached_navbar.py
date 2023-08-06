from django import template
from ..service.get_base_template_cache_time import get_base_template_cache_time_by_part

register = template.Library()


@register.inclusion_tag('base_template/cached_navbar.html')
def cached_navbar():
    cached_navbar_time = get_base_template_cache_time_by_part('NAVBAR')
    return {"cached_navbar_time": cached_navbar_time}