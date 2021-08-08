from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email',)}),
        (_('シフト'),{'fields':('post',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff','post_summary')
    search_fields = ('username',)
    filter_horizontal = ('user_permissions','post',)
    
    def post_summary(self, obj):
        qs = obj.post.all()
        label = ', '.join(map(str, qs))
        return label
    
from django import forms

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('date',)
    search_fields = ( 'date',)
    ordering = ('-date',)
    list_filter = ('date',)
    

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
