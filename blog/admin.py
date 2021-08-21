from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter
import datetime



class PostInline(admin.TabularInline):
    model = models.Post
    fields = ('date', 'start_time','end_time')
    extra = 0

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
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
   
from django import forms

class PublishedListFilter(admin.SimpleListFilter):
    title = '編集'
    parameter_name = 'published'

    def lookups(self, request, model_admin):
        return (
            ('True', '編集可'),
            ('False', '編集不可')
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(published=True)
        elif self.value() == 'False':
            return queryset.filter(published=False)
        else:
            return queryset.all()

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    
    list_select_related = ('name',)
    list_display = ('id','date','start_time','end_time','name','published')
    list_display_links = ('id',)
    #list_editable = ('date','start_time','end_time','name')
    #search_fields = ['date','name__full_name']
    ordering = ('-date',)
    list_filter = (('date', DateRangeFilter), PublishedListFilter, 'name__full_name')
    actions = ["publish", "unpublish"]
    
    def get_rangefilter_date_default(self, request):
        return (datetime.date.today, datetime.date.today)

    def publish(self, request, queryset):
        queryset.update(published=True)

    publish.short_description = "編集可"

    def unpublish(self, request, queryset):
        queryset.update(published=False)

    unpublish.short_description = "編集不可"


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin import AdminSite

class BlogAdminSite(AdminSite):
    site_header = '確認'
    site_title = '確認'
    index_title = 'ホーム'
    site_url = '/dahutos-admin/'
    index_template = 'admin/mypage.html'
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_superuser

mypage_site = BlogAdminSite(name="mypage")
mypage_site.register(models.Post)
mypage_site.register(models.User)
