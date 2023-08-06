from django.db import models
from django.utils import timezone

from djmoney.models.fields import MoneyField
from easy_thumbnails.fields import ThumbnailerImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Price(models.Model):
    STATUS = [
        ('ACTIVE', 'Действующий'),
        ('DELETED', 'Удалено'),
    ]

    cost = MoneyField(
        "Цена"
        , max_digits=10
        , decimal_places=2
        , default_currency='RUB'
    )

    title = models.CharField(
        max_length=50
        , verbose_name="Наименование"
        , null=False
        , default="Услуга"
        , help_text="наименование услуги"
        , db_index=True
    )

    description = RichTextUploadingField(
        verbose_name = "Описание"
        , null = False
        , default = "Эта услуга позволит вам жить лучше"
        , help_text = "Описание услуги"
    )

    image = ThumbnailerImageField(
        upload_to='price/images/%Y/%m/%d/'
        , verbose_name='image'
        , blank=True
    )

    created_at = models.DateTimeField(
        "Дата создания на сервере"
        , default=timezone.now
        , null=False
    )

    status =  models.CharField(
        max_length=30
        , null=False
        , choices=STATUS
        , help_text="Статус"
        , verbose_name='Статус'
        , default='ACTIVE'
    )

    def __str__(self):
        return f'{self.title} {self.cost}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'