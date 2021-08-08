from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from blog.admin import mypage_site

from blog import views

from blog.models import Post

from django.contrib.auth.models import Group

admin.site.site_title = '管理'
admin.site.site_header = 'システム管理サイト'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)
#admin.site.disable_action('delete_selected')
# 実はページを表示するだけならこのように1行で書くことが出来ます。

urlpatterns = [
    path('dahutos-admin/', admin.site.urls),
    path("", login_required(views.Index.as_view()), name="index"),
    path('', include("django.contrib.auth.urls")),
    path("sign-up/", views.SignUpView.as_view(), name="signup"),
    path('month_with_forms/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('month_with_forms/<int:year>/<int:month>/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('detail/<pk>', views.Detail.as_view(), name="detail"),
    path('update/<pk>', views.Update.as_view(), name="update"),
    path('delete/<pk>', views.Delete.as_view(), name="delete"),
    path('mypage/', mypage_site.urls),
    #path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
]
