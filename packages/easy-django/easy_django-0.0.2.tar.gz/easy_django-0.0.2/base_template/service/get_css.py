from ..models import CSS


def get_csss():
    return CSS.objects.all()