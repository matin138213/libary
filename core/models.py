import re

from django.db import models
from rest_framework.exceptions import ValidationError



# from book.models import Books
# from django.apps import apps
# apps.get_model("book", "Books")


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    telegram_id = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def is_valid_iranian_mobile(self):
        pattern = r'^09[0-9]{9}$'
        return re.match(pattern, self.phone_number)

    def clean(self):
        super().clean()
        if not self.is_valid_iranian_mobile():
            raise ValidationError({'phone_number': 'شماره موبایل وارد شده معتبر نمی‌باشد.'})


class Request(models.Model):
    RENEWAL_TYPE = 'R'
    LOAN_TYPE = 'L'
    DELIVER_TYPE = 'D'
    TYPE_CHOICES = (
        (RENEWAL_TYPE, 'renewal'),
        (LOAN_TYPE, 'loan'),
        (DELIVER_TYPE, 'deliver'),
    )
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.CharField(max_length=200, verbose_name='over_data')
    is_accepted = models.CharField(max_length=100)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default=LOAN_TYPE)
