from django.db import models
from django.apps.config import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser,UserManager
import datetime
from django.utils import timezone
from django.urls import reverse_lazy

class UserManager(UserManager):
    pass

class User(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)
    class Meta:
        verbose_name = verbose_name_plural = _('アカウント')


class Category(models.Model):
    name = models.CharField(
    max_length=255,
    blank=True,
    null=True,
    unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = _('カテゴリー')

class Post(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="作成日",
        )

    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="最終更新日",
        )
    body = models.TextField(
        blank=True,
        null=False,
        verbose_name="備考",
        )
        
    time_list=((1,'9:00'),(2,'10:00'),(3,'11:00'),(4,'12:00'),(5,'13:00'),
             (6,'14:00'),(7,'15:00',),(8,'16:00'),(9,'17:00'),(10,'18:00'),
             (11,'19:00'),(12,'20:00'),(13,'21:00'),(14,'22:00'),(15,'23:00'),
             (16,'24:00')
            )
            
    start_time = models.CharField('開始',
        null=True,
        blank=True,
        choices=time_list,
        max_length=255,
        )
        
    end_time = models.CharField('終了',
        null=True,
        blank=True,
        choices=time_list,
        max_length=255,)
        
    date = models.DateTimeField('日付',
        null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリ",
        )

    def __str__(self):
        return self.category
    
    def get_absolute_url(self):
        return reverse_lazy("index")

    class Meta:
        verbose_name = verbose_name_plural = _('投稿')
