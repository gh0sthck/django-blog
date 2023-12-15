from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """Posts (articles) in blog."""

    class Status(models.TextChoices):
        DRAFT = "DF", "Черновик"
        PUBLISHED = "PB", "Опубликовано"

    TITLE_LENGTH: int = 90

    title = models.CharField(max_length=TITLE_LENGTH, verbose_name="Заголовок")
    slug = models.SlugField(max_length=TITLE_LENGTH, verbose_name="Слаг")
    text = models.TextField(verbose_name="Содержание поста")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="Автор")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-publish"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_detail_slug",
            # args=[self.id]
            args=[self.slug]
        )