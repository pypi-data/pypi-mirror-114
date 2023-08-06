from django.urls import path
from django.conf.urls import url
from .views import test

urlpatterns = [

    path(
        "test/"
        , test
        , name="test"
    ),

]
