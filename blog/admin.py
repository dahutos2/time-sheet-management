from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

@admin.register(models.User)
class UserAdmin(UserAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Start)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.End)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


from django import forms

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'category', 'created', 'updated',)
    list_select_related = ('category', )
    list_editable = ( 'category',)
    search_fields = ('category__name', 'created', 'updated',)
    ordering = ('-updated', '-created')
    list_filter = ('category','created', 'updated',)


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
mypage_site.register(models.Category)
