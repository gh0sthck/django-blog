from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

from .models import Post


def home_page(request):
    all_posts: QuerySet[Post] = Post.objects.all()

    txt = ""

    for post in all_posts:
        txt += "{} {} {}<br/>---------------<br/>{}<br/>".format(post.title, post.publish,
                                                      post.author, post.text)
    return render(request, )
    # return HttpResponse("".join(
    #     f"{post.title} {post.publish} {post.author}<br/>---------------<br/>{post.text}<br/>" for post in all_posts
    # ))


def test_page(request):
    published_posts = Post.objects.filter(status=Post.Status.PUBLISHED)  # get already published posts

    return HttpResponse("".join(f"{post.title}<br/>" for post in published_posts))