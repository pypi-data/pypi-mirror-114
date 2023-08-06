=====
easy_django
=====


Quick start
-----------
1. from base_configurations.base_configurations import *
2. INSTALLED_APPS += BASE_INSTALLED_APPS
3. MIDDLEWARE += BASE_MIDDLEWARE
4. Для всех шаблонов наследоваться {% extends 'base_template/base.html' %}
5. urlpatterns += base_urlpatterns (from base_configurations.urlpatterns import base_urlpatterns)
6. settings.py (from base_configurations.base_configurations import *)

6.1. INSTALLED_APPS
-------------------
BASE_INSTALLED_APPS = [
    'base_template',
    'base_navbar',
    'contacts',
    'posts',
    'image_objects',
    'price',
    'ckeditor',
    'ckeditor_uploader',
    'djmoney',
    'easy_thumbnails',
]

6.2. Django cache
-----------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

6.3. CKEDITOR
-------------
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {'default':
    {
        'toolbar': 'None'
        , 'height': '100%'
        , 'width': '100%'
    },
    'extraPlugins': ','.join([
        'uploadimage',  # the upload image feature
        # your extra plugins here
        'div',
        'autolink',
        'autoembed',
        'embedsemantic',
        'autogrow',
        # 'devtools',
        'widget',
        'lineutils',
        'clipboard',
        'dialog',
        'dialogui',
        'elementspath',
        'youtube'
    ]),
}
6.4. django-money
-----------------
CURRENCIES = ('RUB',)

6.5. easy_thumbnail (для базовых приложений)
--------------------------------------------
THUMBNAIL_ALIASES = {
    '': {
        'image_object_card': {'size': (800, 800), 'crop': True},
        'image_card': {'size': (800, 800), 'crop': True},
        'image_galary': {'size': (300, 300), 'crop': True},
        'price_card': {'size': (800, 800), 'crop': True},
    },
}
