from msilib.schema import CustomAction
from django.contrib import admin

from .models import Blog, Comment, Category, CustomUser, Likes, LikesComment

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined")
    search_fields = ('username', 'email')
    
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "created_at", "image", "reading_duration")
    search_fields = ('title', "category")
    list_filter = ('category', "created_at")
    list_display_links = ('title', 'category')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "comment", "created_at", "parent")
    list_filter = ('post', "created_at")
    
class LikesAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    
class LikesCommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "comment", "created_at")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(LikesComment, LikesCommentAdmin)