from django.urls import path

from .views import all_posts_page, post_detail_page

urlpatterns: list = [
    path("", all_posts_page, name="all_posts_page"),
    path("<int:post_id>/", post_detail_page, name="post_detail_page")
]