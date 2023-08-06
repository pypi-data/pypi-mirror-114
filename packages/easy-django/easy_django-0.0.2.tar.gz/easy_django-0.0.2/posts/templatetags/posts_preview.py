from django import template
from ..util import get_config, get_posts_preview_cache_time
from ..service.get_posts_list import get_post_list

register = template.Library()


@register.inclusion_tag('posts/posts_preview.html')
def posts_preview():
    return {
        "posts_list": get_post_list(3)
        , 'config': get_config()
        , 'posts_preview_cache_time': get_posts_preview_cache_time()
    }