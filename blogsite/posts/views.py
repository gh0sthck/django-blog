from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .forms import EmailPostForm, CommentPostForm
from .models import Post, Comments


def all_posts_page(request):
    all_posts: QuerySet[Post] = Post.objects.all()

    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get("page", 1)

    try:
        all_posts = paginator.page(page_number)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return render(request, "index.html", {"title": "главная", "postss": all_posts})


def post_detail_page(request, post_id: int) -> render:
    try:
        current_post: Post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found.")
    else:
        return render(request, "post_detail.html", {"post": current_post})


def post_detail_slug(request, post) -> render:
    post: Post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post)
    comms: QuerySet[Comments] = Comments.objects.filter(post=post, is_active=True)

    if request.method == "POST":
        form = CommentPostForm(request.POST)
        if form.has_changed():
            form.save()
    else:
        form = CommentPostForm()

    return render(request, "post_detail.html", {"post": post, "comments": comms,
                                                "current_user": request.user, "form": form})


def post_share(request, post_id: int) -> render:
    post: Post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            sent = True
    else:
        form = EmailPostForm()

    return render(request, "post_share.html", {"post": post, "form": form, "sent": sent})


def user_page(request, user_id: int) -> render:
    try:
        current_user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    else:
        return render(request,
                      "user_page.html",
                      {"username": current_user.username})
