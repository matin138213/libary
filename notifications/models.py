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
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,blank=True)


class Comment(models.Model):
    star = models.CharField(max_length=5)
    description = models.TextField()
    book = models.ForeignKey("book.Books", on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,blank=True)


class TimeLimit(models.Model):
    book = models.ForeignKey("book.Books", on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL,null=True,blank=True)
    end_time = models.DateTimeField(auto_now_add=True)
    IS_EXTENDED = models.BooleanField()
