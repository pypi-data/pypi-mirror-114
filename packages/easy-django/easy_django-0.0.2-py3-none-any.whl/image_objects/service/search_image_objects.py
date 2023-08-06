from ..models import ImageObject
from django.db.models import Q
import pytz
import datetime


def search_image_objects(last_days: int, string: str, quantity: int):
    if last_days > 737938:
        last_days = 737938
    now = datetime.datetime.now(tz=pytz.UTC)
    last_days_delta = datetime.timedelta(days=last_days)
    last_days = now - last_days_delta

    image_objects = ImageObject.objects.filter(
        date__range=(last_days, now)
        , status='ACTIVE'
    ).filter(
        Q(title__contains=string) |
        Q(description__contains=string) |
        Q(tags__contains=string)
    ).order_by('-date')[:quantity]
    image_objects = image_objects

    return image_objects
