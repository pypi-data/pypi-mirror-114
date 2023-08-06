from django.db import models


CONTACT_TYPE = [
    ('fab fa-vk', 'Вконтакте'),
    ('fab fa-facebook', 'Facebook'),
    ('fab fa-whatsapp', 'whatsApp'),
    ('fab fa-telegram', 'Telegram'),
    ('fab fa-instagram', 'Instagram'),
    ('fas fa-map-marker-alt', 'Геолокация'),
]


STATUS = [
    ('DRAFT', 'Draft'),
    ('ACTIVE', 'Active'),
    ('DELETED', 'Deleted'),
]


class Contact(models.Model):
    link = models.URLField(
        verbose_name="Ссылка"
    )
    contact_type = models.CharField(
        verbose_name="Тип контакта"
        , choices=CONTACT_TYPE
        , max_length=50
    )
    status = models.CharField(
        verbose_name="Статус контакта"
        , choices=STATUS
        , max_length=50
    )
    size = models.IntegerField(
        verbose_name="Размер"
        , default=2
    )
    style = models.CharField(
        verbose_name="Дополнительный css стиль"
        , default=''
        , max_length=500
    )
    order = models.IntegerField(
        verbose_name="Порядок отображения"
        , default=1
    )

    extraclass = models.CharField(
        verbose_name="Дополнительный класс для кастомизации"
        , default=''
        , max_length=500
    )

    def __str__(self):
        return f'{self.contact_type} {self.link}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
