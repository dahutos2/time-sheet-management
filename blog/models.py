from django.db import models
from django.apps.config import AppConfig
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(
    max_length=255,
    blank=False,
    null=False,
    unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('カテゴリー')
        verbose_name_plural = _('カテゴリー')


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('タグ')
        verbose_name_plural = _('タグ')

from django.urls import reverse_lazy

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

    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="タイトル",
        )

    body = models.TextField(
        blank=True,
        null=False,
        verbose_name="本文",
        help_text="HTMLタグは使えません。",
        )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリ",
        )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="タグ",
        )

    published = models.BooleanField(
        default=True,
        verbose_name="公開する",
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])

    class Meta:
        verbose_name = _('投稿')
        verbose_name_plural = _('投稿')
