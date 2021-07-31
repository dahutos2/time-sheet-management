from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from registration import views

from django.contrib.auth.models import Group

admin.site.site_title = '匿名ブログ 内部管理サイト'
admin.site.site_header = '匿名ブログ 内部管理サイト'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)
admin.site.disable_action('delete_selected')
# 実はページを表示するだけならこのように1行で書くことが出来ます。
#index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
    path('dahutos-admin/', admin.site.urls),
    path('', include("blog.urls")),
    #path("", login_required(index_view), name="index"),
    #path('', include("django.contrib.auth.urls")),
    #path("signup/", views.SignUpView.as_view(), name="signup"),
    #path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
]
