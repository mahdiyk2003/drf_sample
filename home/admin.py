from django.contrib import admin
from .models import Post,Comment,Like
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'is_active')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'post')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'post')