from django import template
from ..util import get_config
from base_template.service.get_base_template_cache_time import get_base_template_cache_time_by_part
from ..service.search_image_objects import search_image_objects

register = template.Library()


@register.inclusion_tag('image_objects/preview.html')
def image_objects_preview(quantity: int):
    return {
        "image_objects": search_image_objects(last_days=3650, string='', quantity=quantity)
        , 'config': get_config()
        , 'io_preview_cache_time': get_base_template_cache_time_by_part('IO_PREVIEW')
    }