from django import forms

from .models import Comments, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["text"]


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=120, label="")


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "status", "tags"]