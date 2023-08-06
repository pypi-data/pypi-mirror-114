from django import template

from ..util import get_price_preview_cache_time, get_config
from ..service import get_price_list

register = template.Library()


@register.inclusion_tag('price/templatetags/price_list_preview.html')
def price_preview():
    return {
        "list_price": get_price_list()
        , 'config': get_config()
        , 'price_preview_cache_time': get_price_preview_cache_time()
    }
