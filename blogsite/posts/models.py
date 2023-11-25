from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Posts (articles) in blog."""

    class Status(models.TextChoices):
        DRAFT = "DF", "Черновик"
        PUBLISHED = "PB", "Опубликовано"

    TITLE_LENGTH: int = 90

    title = models.CharField(max_length=TITLE_LENGTH)
    slug = models.SlugField(max_length=TITLE_LENGTH)
    text = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-publish"]

    def __str__(self) -> str:
        return self.title
