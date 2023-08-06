from django.conf import settings
from base_template.service.get_base_template_cache_time import get_base_template_cache_time_by_part


def get_config():
    try:
        config = settings.POSTS_CONFIG
    except:
        config = {
            "buttons": {
                "search": "Искать"
                , 'source_link': "Источник"
                , "more": "Подробнее"
            },
            "not_found_description": "По вашему запросу постов не найдено",
            "default_last_days": 737938,
            "keywords": "posts",
            "posts_list_title": "Новости"
        }
    return config


def get_posts_view_cache_time():
    obj = get_base_template_cache_time_by_part('POSTS_VIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']
    return seconds


def get_posts_preview_cache_time():
    obj = get_base_template_cache_time_by_part('POSTS_PREVIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']

    return seconds