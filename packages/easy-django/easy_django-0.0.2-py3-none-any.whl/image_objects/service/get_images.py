from ..models import Image


def get_images_by_image_object_id(image_object_id, status=None):
    if status == None:
        images = Image.objects.filter(
            image_object__pk=image_object_id
        ).order_by('status', 'uploaded_at')
    else:
        images = Image.objects.filter(
            image_object__pk=image_object_id
            , status=status
        ).order_by('status', 'uploaded_at')
    return images


def get_images(quantity=100):
    images = Image.objects.filter(
        status='ACTIVE'
    ).order_by('order', 'uploaded_at')
    return images

