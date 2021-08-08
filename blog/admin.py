from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class PostInline(admin.TabularInline):
    model = models.Post
    fields = ('date', 'start_time','end_time')
    extra = 1

@admin.register(models.User)
class UserAdmin(UserAdmin):
    inlines = [PostInline]
    fieldsets =(
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)
    
    def has_delete_permission(self,request,obj=None):
        return False
   
from django import forms


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('id','date','start_time','end_time','name')
    list_select_related = ('name',)
    list_display_links = ('id',)
    list_editable = ('date','start_time','end_time','name')
    search_fields = ( 'date','name')
    ordering = ('-date',)
    list_filter = ('date','name')
    

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
