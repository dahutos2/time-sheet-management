from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from time_sheet import views
from time_sheet.models import Post
from django.contrib.auth.models import Group

admin.site.site_title = "管理"
admin.site.site_header = "システム管理サイト"
admin.site.index_title = "メニュー"
admin.site.unregister(Group)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_required(views.Index.as_view()), name="index"),
    path("", include("django.contrib.auth.urls")),
    path("sign-up/", views.SignUpView.as_view(), name="signup"),
    path("user_update/<slug:pk>", views.UserUpdate.as_view(), name="user_update"),
    path(
        "month_with_forms/",
        views.MonthWithFormsCalendar.as_view(),
        name="month_with_forms",
    ),
    path(
        "month_with_forms/<int:year>/<int:month>/",
        views.MonthWithFormsCalendar.as_view(),
        name="month_with_forms",
    ),
    path("index/", views.IndexPost.as_view(), name="index_post"),
    path(
        "index/<int:year>/<int:month>/<int:day>/",
        views.IndexPost.as_view(),
        name="index_post",
    ),
    path("update/<pk>", views.Update.as_view(), name="update"),
    path("delete/<pk>", views.Delete.as_view(), name="delete"),
    path("mypage/", views.Mypage.as_view(), name="mypage"),
    path("mypage/user_shift/<pk>", views.UserShift.as_view(), name="user_shift"),
    path("import/", views.ShiftImport.as_view(), name="import"),
    path("shift/", views.ShiftView.as_view(), name="shift"),
    path(
        "shift/<int:year>/<int:month>/<int:day>/",
        views.ShiftView.as_view(),
        name="shift",
    ),
    path("shift/update/<pk>", views.ShiftUpdate.as_view(), name="shift_update"),
    path("shift/delete/<pk>", views.ShiftDelete.as_view(), name="shift_delete"),
    path("shift/index/", views.ShiftIndex.as_view(), name="shift_index"),
]
