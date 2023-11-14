import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.
class Users(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    username = models.CharField(max_length=255, unique=True, verbose_name='کاربر')
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    email = models.EmailField(verbose_name='ایمیل')
    telegram_id = models.CharField(max_length=100, verbose_name='ایدی تلگرام')
    password = models.CharField(max_length=255, verbose_name='پسورد')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def is_valid_iranian_mobile(self):
        pattern = r'^09[0-9]{9}$'
        return re.match(pattern, self.phone_number)

    def clean(self):
        super().clean()
        if not self.is_valid_iranian_mobile():
            raise ValidationError({'phone_number': 'شماره موبایل وارد شده معتبر نمی‌باشد.'})


class Request(models.Model):
    RENEWAL_TYPE = 'R'
    BORROW_TYPE = 'B'
    DELIVER_TYPE = 'D'
    TYPE_CHOICES = (
        (RENEWAL_TYPE, 'renewal'),
        (BORROW_TYPE, 'borrow'),
        (DELIVER_TYPE, 'deliver'),
    )
    ACCEPTED = 'A'
    NOT_ACCEPTED = 'N'
    PENDING = 'P'
    ACCEPTED_CHOICES = (
        (ACCEPTED, 'accepted'),
        (NOT_ACCEPTED, 'not accepted'),
        (PENDING, 'pending'),
    )
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE, related_name='request', verbose_name='کتاب')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='request', verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساختن')
    meta_data = models.CharField(max_length=200, verbose_name='over_data')
    is_accepted = models.CharField(choices=ACCEPTED_CHOICES, max_length=1, default=PENDING, verbose_name='درخواست')
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default=BORROW_TYPE, verbose_name='نوع')

    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست ها'
