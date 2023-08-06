from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


base_urlpatterns = [
    path('admin/', admin.site.urls)
    , path("ckeditor/", include('ckeditor_uploader.urls'))
    
    , path("posts/front/", include("posts.front_urls"))
    , path("price/front/", include("price.front_urls"))
    , path("image_objects/front/", include("image_objects.front_urls"))
]

base_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
