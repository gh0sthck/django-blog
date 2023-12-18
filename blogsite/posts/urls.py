from django.urls import path

from .views import all_posts_page, post_detail_page, user_page, post_detail_slug, post_share

urlpatterns: list = [
    path("", all_posts_page, name="all_posts_page"),
    # path("<int:post_id>/", post_detail_page, name="post_detail_page"),
    path("<slug:post>", post_detail_slug, name="post_detail_slug"),
    path("profile/<int:user_id>/", user_page, name="user_page"),
    path("share/<int:post_id>/", post_share, name="post_share"),
]