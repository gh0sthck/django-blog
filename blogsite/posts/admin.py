from django.contrib import admin

from .models import Post, Comments


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "text"]
    prepopulated_fields = {"slug": ("title", )}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comments)
class AdminComments(admin.ModelAdmin):
    list_display = ["author", "post", "created", "is_active"]
    list_filter = ["is_active", "created", "updated"]
    search_fields = ["author", "text"]