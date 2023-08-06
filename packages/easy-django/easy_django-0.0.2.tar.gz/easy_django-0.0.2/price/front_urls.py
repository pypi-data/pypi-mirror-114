from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PriceList
from .util import get_price_view_cache_time


urlpatterns = [
    path(
        "list"
         , cache_page(timeout=get_price_view_cache_time(), key_prefix='price_list_view')(PriceList.as_view())
        , name="front_price_list"
    )
    ,
]
