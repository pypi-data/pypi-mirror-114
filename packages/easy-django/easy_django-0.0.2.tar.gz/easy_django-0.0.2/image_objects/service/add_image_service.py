from ..models import ImageObject, Image


def add_image_service(request, image_object_id):
    image = Image.objects.create(
        title=request.POST['title']
        , tag=request.POST['tag']
        , image=request.FILES['image']
        , image_object=ImageObject.objects.get(pk=image_object_id)
        , status=request.POST['status']
    )
    return image