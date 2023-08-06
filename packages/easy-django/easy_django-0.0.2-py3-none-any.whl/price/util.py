from django.conf import settings
from base_template.service.get_base_template_cache_time import get_base_template_cache_time_by_part


def get_config():
    try:
        config = settings.PRICE_CONFIG
    except:
        config = {
            "price_navbar": "Прайс-лист",
            "price_list_title": "Прайс-лист"
        }
    return config


def get_price_view_cache_time():
    obj = get_base_template_cache_time_by_part('PRICE_VIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']
    return seconds


def get_price_preview_cache_time():
    obj = get_base_template_cache_time_by_part('PRICE_PREVIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']

    return seconds