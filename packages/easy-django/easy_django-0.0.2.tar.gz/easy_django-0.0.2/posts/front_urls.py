from django.urls import path
from django.views.decorators.cache import cache_page

from .front_views.post_detail_view import PostDetailView
from .front_views.post_list_view import PostsListView

from .util import get_posts_view_cache_time


urlpatterns = [
    path(
        "detail/"
        "<int:post_id>/"
        , cache_page(timeout=get_posts_view_cache_time(), key_prefix='post_detail_view')(PostDetailView.as_view())
        , name="post_detail"
    ),

    path(
        "list/"
        , PostsListView.as_view()
        , name="posts_list"
    ),
]
