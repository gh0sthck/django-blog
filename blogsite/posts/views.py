from django.db.models import QuerySet
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Post


def all_posts_page(request):
    all_posts: QuerySet[Post] = Post.objects.all()

    return render(request, "index.html", {"title": "главная", "posts": all_posts})


def post_detail_page(request, post_id: int) -> render:
    try:
        current_post: Post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found.")
    else:
        return render(request,
                      "post_detail.html",
                      {"post_title": current_post.title, "post_description": current_post.text})