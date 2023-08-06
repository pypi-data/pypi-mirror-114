from ..models import Posts
from django.db.models import Q
import pytz
import datetime


def search_posts(string: str, last_days: int, quantity=20):
    if last_days > 737938:
        last_days = 737938
    now = datetime.datetime.now(tz=pytz.UTC)
    last_days_delta = datetime.timedelta(days=last_days)
    last_days = now - last_days_delta

    posts = Posts.objects.filter(
        post_date__range=(last_days, now)
    )

    posts = posts.filter(
        Q(post_header__contains=string) |
        Q(post_content__contains=string)
    ).order_by('-post_date')[:quantity]

    return posts