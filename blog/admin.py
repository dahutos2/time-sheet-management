from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

@admin.register(models.User)
class UserAdmin(UserAdmin):
    pass

from django import forms

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'created', 'updated',)
    search_fields = ( 'created', 'updated',)
    ordering = ('-updated', '-created')
    list_filter = ('created', 'updated',)


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin import AdminSite

class BlogAdminSite(AdminSite):
    site_header = 'マイページ'
    site_title = 'マイページ'
    index_title = 'ホーム'
    site_url = None
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active


mypage_site = BlogAdminSite(name="mypage")
mypage_site.register(models.Post)
mypage_site.register(models.User)
