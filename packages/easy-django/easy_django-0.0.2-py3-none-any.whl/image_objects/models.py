from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from easy_thumbnails.fields import ThumbnailerImageField
from PIL import Image as PilImage

STATUS = [
    ('DRAFT', 'Draft'),
    ('REVIEW', 'Review'),
    ('ACTIVE', 'Active'),
    ('DELETED', 'Deleted'),
    ('REFUSED', 'Refused'),
]


class ImageObject(models.Model):
    user = models.ForeignKey(
        User
        , on_delete=models.PROTECT
        , help_text='Author'
        , verbose_name='Author'
    )

    title = models.CharField(
        max_length=30
        , verbose_name='Title'
    )

    description = RichTextUploadingField(
        verbose_name='Description'
    )

    date = models.DateTimeField(
        default=timezone.now
        , help_text='Date'
        , verbose_name='Date'
    )

    status = models.CharField(
        max_length=30
        , null=False
        , choices=STATUS
        , default='ACTIVE'
    )

    tags = models.CharField(
        max_length=100
        , verbose_name='Tags, "," delimiter'
    )

    def __str__(self):
        return f'{self.title} {self.pk} with tags {self.tags}'

    def get_absolute_url(self):
        return reverse('front_view_image_object', kwargs={'image_object_id': self.pk})

    @property
    def get_images(self):
        return Image.objects.filter(status='ACTIVE', image_object__pk=self.pk).order_by('order')


class Image(models.Model):
    title = models.CharField(
        max_length=30
        , verbose_name='Title image'
    )
    # image = models.ImageField(
    #     upload_to='image_objects/images/%Y/%m/%d/'
    #     , verbose_name='image'
    # )
    image = ThumbnailerImageField(
        upload_to='image_objects/images/%Y/%m/%d/'
        , verbose_name='image'
        , blank=True
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30
        , null=False
        , choices=STATUS
        , default='ACTIVE'
    )

    tag = models.CharField(
        max_length=20
        , verbose_name='Tag'
        , default='tag'
    )

    image_object = models.ForeignKey(
        ImageObject
        , on_delete=models.PROTECT
        , verbose_name='Image object'
        , help_text='Choise object for image'
        , related_name='images'
    )

    order = models.IntegerField(
        verbose_name="Ordering priority"
        , default=1
    )

    def __str__(self):
        return f'Image "{self.title}" with tag "{self.tag}"'

