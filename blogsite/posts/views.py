from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Post


def all_posts_page(request):
    all_posts: QuerySet[Post] = Post.objects.all()

    return render(request, "index.html", {"title": "главная", "postss": all_posts})


def post_detail_page(request, post_id: int) -> render:
    try:
        current_post: Post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found.")
    else:
        return render(request,
                      "post_detail.html",
                      {"post_title": current_post.title, "post_description": current_post.text,
                       "post_pubdate": current_post.publish, "post_author": current_post.author})


def post_detail_slug(request, post) -> render:
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post)

    post_title = post.title
    post_description = post.text
    post_pubdate = post.publish
    post_author = post.author

    return render(request,
                  "post_detail.html",
                  {"post_title": post_title.title, "post_description": post_description,
                   "post_pubdate": post_pubdate, "post_author": post_author})


def user_page(request, user_id: int) -> render:
    try:
        current_user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    else:
        return render(request,
                      "user_page.html",
                      {"username": current_user.username})