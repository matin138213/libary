import random

from django.core.validators import MinValueValidator, MaxValueValidator
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
    title = models.CharField(max_length=100, verbose_name='موضوع')
    description = models.TextField(verbose_name='متن')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساختن')
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL, null=True, related_name='notifications',
                             verbose_name='کاربر')

    class Meta:
        verbose_name = 'اطلاع رسانی'
        verbose_name_plural = 'اطلاع رسانی ها'


class Comment(models.Model):
    star = models.PositiveIntegerField(verbose_name='ستاره', validators=[MinValueValidator(limit_value=1),
                                                                         MaxValueValidator(limit_value=5)])
    description = models.TextField(verbose_name='متن')
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE, related_name='comment', verbose_name='کتب')
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL, null=True, related_name='comment',
                             verbose_name='کاربر')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class TimeLimit(models.Model):
    book = models.ForeignKey("book.Books", on_delete=models.SET_NULL, null=True, related_name='time',
                             verbose_name='تاب')
    user = models.ForeignKey("core.Users", on_delete=models.SET_NULL, null=True, related_name='time',
                             verbose_name='کاربر')
    end_time = models.DateTimeField(verbose_name='مهلت')
    is_extended = models.BooleanField(default=False, verbose_name='درست غلط')

    class Meta:
        verbose_name = 'تایم پایانی'
        verbose_name_plural = 'تایم پایانی ها'
