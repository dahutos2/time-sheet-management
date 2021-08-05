from django.urls import path

from . import views

from .admin import mypage_site

urlpatterns = [
    path('', views.Index.as_view(), name="index"),

    # <pk>にPostのIDを渡すと表示される。
    path('month_with_forms/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('month_with_forms/<int:year>/<int:month>/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('create/', views.Create.as_view(), name="create"),
    path('mypage/', mypage_site.urls),
]
