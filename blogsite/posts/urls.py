from typing import List

from django.urls import path

from .views import all_posts_page, post_detail_slug, posts_with_current_tag, post_create

urlpatterns: List = [
    path("", all_posts_page, name="all_posts_page"),
    path("<slug:post_slug>", post_detail_slug, name="post_detail_slug"),
    path("tag/<slug:tag>", posts_with_current_tag, name="post_with_tag"),
    path("create_post/", post_create, name="create_post"),
]