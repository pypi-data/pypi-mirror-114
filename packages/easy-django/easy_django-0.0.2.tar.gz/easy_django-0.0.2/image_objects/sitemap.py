from django.contrib.sitemaps import Sitemap
from django.urls import reverse

import datetime

from .models import ImageObject


class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['front_list_image_objects',]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime.datetime.now()


class ImageObjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'

    def items(self):
        return ImageObject.objects.filter(status='ACTIVE')

    def lastmod(self, obj):
        return obj.date


def get_image_objects_sitemap():
    return {
        "image_objects": ImageObjectSitemap,
        "image_objects_static": StaticViewSitemap
    }