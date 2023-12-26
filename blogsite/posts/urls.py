from django.urls import path

from .views import all_posts_page, user_page, post_detail_slug, post_share, posts_with_current_tag

app_name = "posts"

urlpatterns: list = [
    path("", all_posts_page, name="all_posts_page"),
    path("<slug:post_slug>/", post_detail_slug, name="post_detail_slug"),
    path("profile/<int:user_id>/", user_page, name="user_page"),
    path("share/<int:post_id>/", post_share, name="post_share"),
    path("tag/<slug:tag>", posts_with_current_tag, name="post_with_tag")
]