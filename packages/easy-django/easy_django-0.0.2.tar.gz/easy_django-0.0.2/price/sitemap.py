from django.contrib.sitemaps import Sitemap
from django.urls import reverse

import datetime


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['front_list_price',]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime.datetime.now()


def get_price_sitemap():
    return {
        "price_static": StaticViewSitemap
    }