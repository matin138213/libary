from django.db import models


# from django.apps import apps
#
# apps.get_model("core", "Users")


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='موضوع')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='والدین')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Books(models.Model):
    owner = models.ForeignKey("core.Users", on_delete=models.SET_NULL, null=True, related_name='book',
                              verbose_name='صاحب')
    publisher = models.CharField(max_length=255, verbose_name='ناشر')
    vol = models.PositiveIntegerField(verbose_name='جلد')
    page_count = models.PositiveIntegerField(verbose_name='تعداد صفحه')
    writer = models.CharField(max_length=255, verbose_name='نویسنده')
    translator = models.CharField(max_length=255,null=True,blank=True, verbose_name='مترجم')
    publish_year = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    # evable_notif = models.ManyToManyField("core.Users", related_name='users', verbose_name='اطلاع رسانی به کاربر')
    category = models.ManyToManyField(Category,related_name='categories', verbose_name='کتگوری')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
