from django.contrib.sitemaps import Sitemap
from django.urls import reverse

import datetime

from .models import Posts


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['posts_list',]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime.datetime.now()


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Posts.objects.filter(status='ACTIVE')

    def lastmod(self, obj):
        return obj.post_date


def get_posts_sitemap():
    return {
        "posts": PostSitemap,
        "posts_static": StaticViewSitemap
    }