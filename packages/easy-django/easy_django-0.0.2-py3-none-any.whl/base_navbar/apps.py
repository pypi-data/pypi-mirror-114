from django.apps import AppConfig


class BaseNavbarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_navbar'
    verbose_name = 'Панель навигации'
