from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
import datetime
from django.urls import reverse_lazy


class UserManager(UserManager):
    pass


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=False, blank=True)
    full_name = models.CharField(
        "氏名",
        null=True,
        max_length=255,
    )

    class Meta:
        verbose_name = verbose_name_plural = _("アカウント")

    def get_absolute_url(self):
        return reverse_lazy("/")

    def __str__(self):
        return str(self.full_name)

    @staticmethod
    def get(username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_help_user():
        return User.get(username=244)


class Post(models.Model):
    time_list = (
        ("1", "9:00"),
        ("2", "10:00"),
        ("3", "11:00"),
        ("4", "12:00"),
        ("5", "13:00"),
        ("6", "14:00"),
        ("7", "15:00"),
        ("8", "16:00"),
        ("9", "17:00"),
        ("10", "18:00"),
        ("11", "19:00"),
        ("12", "20:00"),
        ("13", "21:00"),
        ("14", "22:00"),
        ("15", "23:00"),
        ("16", "24:00"),
    )
    start_time = models.CharField(
        "開始",
        blank=True,
        choices=time_list,
        max_length=255,
    )

    end_time = models.CharField(
        "終了",
        blank=True,
        choices=time_list,
        max_length=255,
    )

    date = models.DateField(
        "日付",
    )

    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="related_user",
        verbose_name="ユーザー",
    )

    published = models.BooleanField(
        default=True,
        verbose_name="編集",
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = verbose_name_plural = _("希望シフト")


class Shift(models.Model):

    start_time = models.TimeField("開始時間", default=datetime.time(0, 0, 0))

    end_time = models.TimeField("終了時間", default=datetime.time(0, 0, 0))

    time = models.TimeField("休憩時間", default=datetime.time(0, 0))

    description = models.TextField("メモ", blank=True)

    date = models.DateField(
        "日付",
    )

    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="related_shift",
        verbose_name="ユーザー",
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = verbose_name_plural = _("完成シフト")
