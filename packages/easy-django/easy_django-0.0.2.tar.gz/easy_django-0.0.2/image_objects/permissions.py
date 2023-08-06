def get_perms_dict(request):
    context = {}
    context['has_perms_image_add'] = request.user.has_perms('image_objects.image.add')
    context['has_perms_image_edit'] = request.user.has_perms('image_objects.image.edit')
    context['has_perms_image_view'] = request.user.has_perms('image_objects.image.view')
    context['has_perms_image_delete'] = request.user.has_perms('image_objects.image.delete')

    context['has_perms_image_object_add'] = request.user.has_perms('image_objects.imageobject.add')
    context['has_perms_image_object_edit'] = request.user.has_perms('image_objects.imageobject.edit')
    context['has_perms_image_object_view'] = request.user.has_perms('image_objects.imageobject.view')
    context['has_perms_image_object_delete'] = request.user.has_perms('image_objects.imageobject.delete')

    return context
