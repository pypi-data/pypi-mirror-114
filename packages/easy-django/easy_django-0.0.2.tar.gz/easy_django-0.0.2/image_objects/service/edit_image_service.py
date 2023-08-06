from ..models import ImageObject, Image


def edit_image_service(request, image_id, form):
    cd = form.cleaned_data
    image = Image.objects.get(pk=image_id)
    image.title = request.POST['title']
    image.status = request.POST['status']
    image = cd['image']
    image.tag = request.POST['tag']
    image.save()

    return image