from ..models import BaseTemplateCacheTime


def get_base_template_cache_time_all():
    return BaseTemplateCacheTime.objects.all()


def get_base_template_cache_time_by_part(part):
    try:
        return BaseTemplateCacheTime.objects.get(base_template_part=part)
    except:
        return {"seconds": 7200}