import random

from django.db import models
# from django.apps import apps

# from book.models import Books
# from core.models import Users
#
# apps.get_model("book", "Books")
#
# apps.get_model("core", "Users")


# Create your models here.
class Notifications(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='images')
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,related_name='notifications')


class Comment(models.Model):
    star = models.PositiveIntegerField()
    description = models.TextField()
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE,related_name='comment')
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,related_name='comment')


class TimeLimit(models.Model):
    book = models.ForeignKey("book.Books", on_delete=models.SET_NULL,null=True,related_name='time')
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,related_name='time')
    end_time = models.DateTimeField()
    is_extended = models.BooleanField(default=False)
