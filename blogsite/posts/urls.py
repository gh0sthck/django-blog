from django.urls import path

from .views import home_page, test_page

urlpatterns: list = [
    path("", home_page),
    path("test", test_page)
]