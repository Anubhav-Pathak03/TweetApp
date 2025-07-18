from django.contrib import admin
from .models import Tweet , Comment

# Register your models here.
# admin.py

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_add')
    search_fields = ('text', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tweet', 'user', 'comment_text', 'timestamp')
    search_fields = ('comment_text', 'user__username', 'tweet__text')
