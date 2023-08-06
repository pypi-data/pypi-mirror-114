from ..models import Font


def get_fonts():
    return Font.objects.all()