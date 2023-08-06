from ..models import Navbar
from django.core.exceptions import ObjectDoesNotExist


def get_navbar():
    try:
        return Navbar.objects.filter(is_enabled=True).select_related()[0]
    except:
        return None