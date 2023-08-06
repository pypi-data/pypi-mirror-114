from ..models import Posts


def get_post_list(quantity: int):
    posts = Posts.objects.filter(
        status="ACTIVE"
    ).order_by('-post_date')[:quantity]

    return posts