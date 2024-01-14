from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password_repeat(self):
        reg_cleand = self.cleaned_data
        if reg_cleand["password_repeat"] != reg_cleand["password"]:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return reg_cleand["password_repeat"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]


class UserSearchForm(forms.Form):
    search_field = forms.CharField(max_length=120, label="", required=False)