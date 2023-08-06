from django.db import models
from django.shortcuts import reverse

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

from ckeditor_uploader.fields import RichTextUploadingField


STATUS = [
    ('DRAFT', 'Черновик'),
    ('REVIEW', 'Рассмотрение'),
    ('ACTIVE', 'Действующий'),
    ('DELETED', 'Удалено'),
    ('REFUSED', 'Отклонено'),
]


class Posts(models.Model):

    status = models.CharField(
        max_length=30
        , null=False
        , choices=STATUS
        , help_text="Статус"
        , verbose_name='Статус'
    )

    source = models.URLField(
        verbose_name="Источник"
        , null=False
        , default='yandex.com'
    )

    post_date = models.DateTimeField(
        verbose_name="Дата поста"
    )

    post_header = models.CharField(
        verbose_name="Заголовок"
        , max_length=100
        , null=False
        , default="Заголовок"
    )

    post_content_preview = models.CharField(
        verbose_name="Краткое содержание"
        , max_length=300
        , null=False
        , default="Краткое содержание"
    )

    post_content = RichTextUploadingField(
        verbose_name="Содержание поста"
        , null=False
        , default="Содержание"
    )

    image = ThumbnailerImageField(
        upload_to='posts/images/%Y/%m/%d/'
        , verbose_name='image'
        , blank=True
    )

    def __str__(self):
        return f'{self.pk} : {self.post_header}'

    @property
    def get_image_url(self):
        options = {'size': (640, 640), 'crop': True}
        thumb_url = get_thumbnailer(self.image).get_thumbnail(options).url
        return thumb_url

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk})
