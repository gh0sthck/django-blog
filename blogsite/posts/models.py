from django.contrib.auth.models import User
from django.db import models
from pytils.translit import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


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
    tags = TaggableManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-publish"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            print("slug", self.slug)
        super(Post, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_detail_slug",
            args=[self.slug]
        )


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комменатрии"
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"<Comment by {self.author.username} on {self.post}>"