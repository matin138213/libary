import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


# from book.models import Books
# from django.apps import apps
# apps.get_model("book", "Books")


# Create your models here.
class Users(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    telegram_id = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

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
        (ACCEPTED , 'accepted'),
        (NOT_ACCEPTED , 'not accepted'),
        (PENDING, 'pending'),
    )
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE,related_name='request')
    user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='request')
    created_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.CharField(max_length=200, verbose_name='over_data')
    is_accepted = models.CharField(choices=ACCEPTED_CHOICES,max_length=1,default=PENDING)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default=BORROW_TYPE)
