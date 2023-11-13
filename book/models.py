from django.db import models

# from django.apps import apps
#
# apps.get_model("core", "Users")


# Create your models here.
class Books(models.Model):
    owner = models.ForeignKey("core.Users", on_delete=models.CASCADE)
    publisher = models.CharField(max_length=255)
    vol = models.PositiveIntegerField()
    page_count = models.PositiveIntegerField()
    writer = models.CharField(max_length=255)
    translator = models.CharField(max_length=255)
    publish_year = models.CharField(max_length=255)
    stock = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    picture = models.ImageField(upload_to='images')
    evable_notif = models.ManyToManyField("core.Users", related_name='users')


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,blank=True)
    book = models.ManyToManyField("book.Books", related_name='books')
