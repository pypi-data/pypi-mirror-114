from django.urls import path
from django.views.decorators.cache import cache_page

from .views.front.image_objects.list import ListImageObjects
from .views.front.image_objects.view import ViewImageObject

from .util import get_io_view_cache_time


urlpatterns = [
    path(
        "view/"
        "<int:image_object_id>/"
        , cache_page(timeout=get_io_view_cache_time(), key_prefix='view_image_object')(ViewImageObject.as_view())
        , name="front_view_image_object"
    )
    ,
    path(
        "list/"
        , ListImageObjects.as_view()
        , name="front_list_image_objects"
    )
    ,
]
