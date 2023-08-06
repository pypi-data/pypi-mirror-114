from django import template
from ..service.get_images import get_images
from ..util import get_galary_cache_time, get_config

register = template.Library()


@register.inclusion_tag('image_objects/templatetags/galary.html')
def image_galary():
    return {
        "images": get_images(),
        "config": get_config(),
        "galary_cache_time": get_galary_cache_time()
    }