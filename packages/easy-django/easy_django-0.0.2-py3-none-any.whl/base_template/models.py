from django.db import models
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

BASE_TEMPLATE_PART = [
    ('HEAD', 'Head'),
    ('BODY', 'Body'),
    ('NAVBAR', 'Navbar'),

    ('IO_PREVIEW', 'Image objects preview'),
    ('IO_VIEW', 'Image objects view'),
    ('IO_GALARY', 'Image objects galary'),

    ('POSTS_PREVIEW', 'Posts preview'),
    ('POSTS_VIEW', 'Posts view'),

    ('PRICE_VIEW', 'Price view'),
    ('PRICE_PREVIEW', 'Price preview'),
]

ANALYTICAL_SERVICES = [
    ('YANDEX_METRIKA_COUNTER_ID', 'YANDEX_METRIKA_COUNTER_ID'),
    ('GOOGLE_ANALYTICS_GTAG_PROPERTY_ID', 'GOOGLE_ANALYTICS_GTAG_PROPERTY_ID'),
]

WEB_MASTER_SERVICES = [
        ('yandex-verification', 'yandex-verification'),
        ('google-site-verification', 'google-site-verification'),
    ]


class HTMLHeadLink(models.Model):

    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This link is needed for ..."
    )

    content = models.TextField(
        verbose_name="Head link content"
        , null=False
        , default="This code snippet will be inserted into the head section of the base template"
        , help_text="This code snippet will be inserted into the head section of the base template"
        , unique=True
    )

    order = models.PositiveSmallIntegerField(
        verbose_name="Sort order"
        , null=False
        , default=1
        , help_text="Ordering in template"
    )

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = 'Head link'
        verbose_name_plural = 'Head links'


class HTMLHeadMeta(models.Model):

    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This meta is needed for ..."
    )

    content = models.TextField(
        verbose_name="Head meta content"
        , null=False
        , default="This code snippet will be inserted into the head section of the base template"
        , help_text="This code snippet will be inserted into the head section of the base template"
        , unique=True
    )

    order = models.PositiveSmallIntegerField(
        verbose_name="Sort order"
        , null=False
        , default=1
        , help_text="Ordering in template"
    )

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = 'Head meta'
        verbose_name_plural = 'Head meta'


class HTMLBodyScript(models.Model):

    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This script is needed for ..."
    )

    content = models.TextField(
        verbose_name="Body script content"
        , null=False
        , default="This code snippet will be inserted into the body section of the base template"
        , help_text="This code snippet will be inserted into the body section of the base template"
        , unique=True
    )

    order = models.PositiveSmallIntegerField(
        verbose_name="Sort order"
        , null=False
        , default=1
        , help_text="Ordering in template"
    )

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = 'HTML скрипт (body)'
        verbose_name_plural = 'HTML скрипты (body)'


class DjangoAnalyticalServices(models.Model):

    service = models.CharField(
        max_length=100
        , null=False
        , choices=ANALYTICAL_SERVICES
        , default='YANDEX_METRIKA_COUNTER_ID'
        , verbose_name="Service"
        , unique=True
    )

    value = models.TextField(
        max_length=100
        , null=False
        , default='80821312'
    )

    def __str__(self):
        return f'{self.service} {self.value}'

    class Meta:
        verbose_name = 'Сервис аналитики'
        verbose_name_plural = 'Сервисы аналитики'


class Favicon(models.Model):
    favicon = ThumbnailerImageField(upload_to='favicon', blank=True)
    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This favicon is needed for ..."
    )
    tile_color = models.CharField(
        verbose_name="TileColor for msapplication and macos"
        , null=False
        , default="#2b5797"
        , max_length=100
    )
    app_name = models.CharField(
        verbose_name="Application name"
        , null=False
        , default="My application"
        , max_length=100
    )
    theme_color = models.CharField(
        verbose_name="Theme color"
        , null=False
        , default="#ffffff"
        , max_length=100
    )

    def get_absolute_url_size(self, size):
        options = {'size': (size, size), 'crop': True}
        thumb_url = get_thumbnailer(self.favicon).get_thumbnail(options).url
        return thumb_url

    def __str__(self):
        return f'{self.label} {self.favicon}'

    class Meta:
        verbose_name = 'Значок сайта'
        verbose_name_plural = 'Значки сайта'


class CSS(models.Model):
    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This css is needed for ..."
    )

    content = models.FileField(
        upload_to='css'
        , verbose_name="file css"
    )

    def __str__(self):
        return f'{self.label} {self.content}'

    @property
    def get_absolute_url_property(self):
        return f'{settings.MEDIA_URL}{self.content}'

    def get_absolute_url(self):
        return f'{settings.MEDIA_URL}{self.content}'

    class Meta:
        verbose_name = 'CSS файл'
        verbose_name_plural = 'CSS файлы'


class Verifications(models.Model):

    service = models.CharField(
        max_length=100
        , null=False
        , choices=WEB_MASTER_SERVICES
        , default='yandex-verification'
        , verbose_name="Service"
        , unique=True
    )

    value = models.TextField(
        max_length=300
        , null=False
        , default='01a933e67426668b'
    )

    def __str__(self):
        return f'{self.service} {self.value}'

    class Meta:
        verbose_name = 'Подтверждение сайта'
        verbose_name_plural = 'Подтверждения сайта'


class BaseTemplateCacheTime(models.Model):

    base_template_part =  models.CharField(
        max_length=100
        , null=False
        , choices=BASE_TEMPLATE_PART
        , default='HEAD'
        , verbose_name="Base template part (unique)"
        , unique=True
        , db_index=True
    )

    seconds = models.IntegerField(
        verbose_name="Value of seconds cache"
    )

    def __str__(self):
        return f'{self.base_template_part} {self.seconds} seconds'

    class Meta:
        verbose_name = 'CACHE-time'
        verbose_name_plural = 'CACHE-time'


class Font(models.Model):
    label = models.TextField(
        verbose_name="Label"
        , max_length=100
        , null=False
        , default="This font is ..."
    )

    content = models.FileField(
        upload_to='fonts'
        , verbose_name="file font"
    )

    def __str__(self):
        return f'{self.label} {self.content}'

    @property
    def get_absolute_url_property(self):
        return f'{settings.MEDIA_URL}{self.content}'

    def get_absolute_url(self):
        return f'{settings.MEDIA_URL}{self.content}'

    class Meta:
        verbose_name = 'Шрифт'
        verbose_name_plural = 'Шрифты'
