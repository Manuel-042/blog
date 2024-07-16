from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from cloudinary.models import CloudinaryField
import math
from django_editorjs import EditorJsField



# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category_name
    
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="the author's id", related_name="blogs")
    description = models.TextField(max_length=100, blank=True, null=True)
    image = CloudinaryField('image')
    blogpost = EditorJsField(editorjs_config={
        "placeholder": "Start writing your story!",
        "tools": {
            "Image": {
                "config": {
                    "endpoints": {
                        "byFile": 'http://127.0.0.1:8000/blog/uploadImageFile/',
                        "byUrl": "http://127.0.0.1:8000/blog/uploadImageUrl/",
                    },
                    "additionalRequestHeaders": [{"Content-Type": 'multipart/form-data'}]
                }
            }
        }
    })
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="the blog's category", related_name="name")
    created_at = models.DateField(default=date.today)
    
    def __str__(self):
        return self.title + " ==> " + str(self.author)
    
    def reading_duration(self):
        word_count = len(self.blogpost.split())
        reading_speed_wpm = 200  # Average reading speed in words per minute
        duration = math.ceil(word_count / reading_speed_wpm)
        return duration

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = "It's optional..."
        return super().save(*args, **kwargs)
    
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="this author's comment", related_name="comments")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="this author's post", related_name="comments")
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies', verbose_name="this comment's parent")

    def __str__(self):
        return self.comment[:20]
    
class Likes(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="this user's like")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes", verbose_name="the liked post")
    created_at = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class LikesComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="this user's like")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comment_likes", verbose_name="the liked post")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", verbose_name="the liked comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)