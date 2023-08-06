from ..models import Verifications


def get_verifications():
    return Verifications.objects.all()