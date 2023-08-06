from django.urls import path
from django.conf.urls import url, handler404
from .views import test



urlpatterns = [

    path(
        "test/"
        , test
        , name="test"
    ),

]
