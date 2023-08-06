from django.conf import settings
from base_template.service.get_base_template_cache_time import get_base_template_cache_time_by_part


def get_config():
    try:
        config = settings.IMAGE_OBJECTS_CONFIG
    except:
        config = {
            "buttons": {
                "search": "Искать"
                , "add_image_object": "Добавить"
                , "list_image_objects": "Список"
                , "home": "Home"
                , "view_image_object": "Просмотр"
                , "edit_image_object": "Изменить"
                , "save_image_object": "Сохранить"
                , "add_image": "Добавить"
                , "list_image": "Список"
                , "save_image": "Сохранить"
                , "edit_image": "Изменить"
            },
            "titles": {
                "search_panel_title": "Примеры"
                , "list_image_objects_title": "Список примеров"
                , "galary": "Галерея"
            },
            "not_found_description": "По вашему запросу примеров не найдено",
            "default_last_days": 737938
            , "keywords": "Примеры"
            , "description": "Примеры"
        }
    return config


def get_io_view_cache_time():
    obj = get_base_template_cache_time_by_part('IO_VIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']

    return seconds


def get_io_preview_cache_time():
    obj = get_base_template_cache_time_by_part('IO_PREVIEW')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']

    return seconds


def get_galary_cache_time():
    obj = get_base_template_cache_time_by_part('IO_GALARY')
    try:
        seconds = obj.seconds
    except:
        seconds = obj['seconds']

    return seconds