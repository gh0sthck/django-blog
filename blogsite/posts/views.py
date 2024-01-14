from typing import List

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag

from .forms import EmailPostForm, CommentPostForm, SearchForm, CreatePostForm
from .models import Post, Comments


def all_posts_page(request):
    form = SearchForm()
    all_posts: QuerySet[Post] = Post.objects.all()
    tags: List = []
    search_query = None

    if "search_query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search_query"]
            all_posts_title: QuerySet[Post] = Post.objects.filter(title__contains=search_query)
            all_posts_tags: QuerySet[Post] = Post.objects.filter(tags__name__search=search_query)
            all_posts_text: QuerySet[Post] = Post.objects.filter(text__search=search_query)
            tags: QuerySet[Tag] = Post.tags.filter(name__contains=search_query)

            all_posts: QuerySet[Post] = all_posts_title.union(all_posts_text, all_posts_tags)

    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get("page", 1)

    try:
        all_posts = paginator.page(page_number)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return render(request, "index.html", {"title": "главная", "postss": all_posts, "form": form,
                                          "tags": tags, "search_query": search_query})


def post_detail_slug(request, post_slug) -> render:
    post: Post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post_slug)
    comments: QuerySet[Comments] = Comments.objects.filter(post=post, is_active=True)
    tags: QuerySet[Tag] = post.tags.all()
    similar_posts: QuerySet[Tag] = post.tags.similar_objects()

    if request.method == "POST":
        form = CommentPostForm(request.POST)
        if form.has_changed():
            aid = form.save(commit=False)
            aid.author_id = request.user.id
            aid.post = Post.objects.get(slug=post_slug)
            aid.save()
            return redirect("post_detail_slug", post_slug)
    else:
        form = CommentPostForm()

    return render(request, "post_detail.html", {"post": post, "comments": comments,
                                                "current_user": request.user, "form": form,
                                                "tags": tags, "similar_posts": similar_posts})


@login_required
def post_create(request) -> render:
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.has_changed():
            author_id = form.save(commit=False)
            author_id.author_id = request.user.id
            author_id.save()
            form.save_m2m()
            return redirect("all_posts_page")
    else:
        form = CreatePostForm()

    return render(request, "post_create.html", {"form": form})


def posts_with_current_tag(request, tag) -> render:
    tag = Tag.objects.get(name=tag)
    post = Post.objects.filter(tags__in=[tag])

    return render(request, "tags_page.html", {"posts": post, "tag": tag})