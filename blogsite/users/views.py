from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render

from .forms import LoginForm


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


def user_page(request, user_id: int) -> render:
    try:
        current_user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    else:
        return render(request,
                      "user_page.html",
                      {"current_user": current_user})