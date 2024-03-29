from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm, UserSearchForm
from .models import Profile


def login_page_for_test(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data["username"], password=clean_data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticate successfully")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()

    return render(request, "user_login.html", {"form": form})


def registration(request) -> render:
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data["password"])
                new_user.save()
                Profile.objects.create(user=new_user)
                return render(request, "user_registration_done.html", {"new_user": new_user})
        else:
            form = RegistrationForm()

        return render(request, "user_registration.html", {"form": form})
    else:
        return redirect("user_page", user_id=request.user.id)


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Изменения сохранены")
        else:
            messages.error(request, "Произошла ошибка")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, "user_edit.html", {"user_form": user_form, "profile_form": profile_form})


def user_page(request, user_id: int) -> render:
    try:
        current_user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    else:
        current_profile: Profile = Profile.objects.get(user=current_user)

        try:
            photo_url = current_profile.photo.url
        except ValueError:
            photo_url = ""

        user_posts = current_user.blog_posts.all()

        return render(request,
                      "user_page.html",
                      {"current_user": current_user, "current_profile": current_profile, "photo_url": photo_url,
                       "user": request.user, "user_posts": user_posts})


def all_users(request) -> render:
    all_usr: QuerySet[User] = User.objects.all()

    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            current_user: QuerySet[User] = User.objects.filter(username__contains=data["search_field"])
            all_usr = current_user
    else:
        form = UserSearchForm()

    return render(request, "all_users.html", {"all_users": all_usr, "form": form})