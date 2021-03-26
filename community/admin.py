from django.contrib import admin
from .models import Review, Comment


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'movie_title', 'rank', 'content', 'created_at', 'updated_at', 'user_id')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'review_id', 'user_id')

admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)