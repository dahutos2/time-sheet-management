from django.urls import path

from . import views

from .admin import mypage_site

urlpatterns = [
    # <pk>にPostのIDを渡すと表示される。
    path('month_with_forms/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('month_with_forms/<int:year>/<int:month>/', views.MonthWithFormsCalendar.as_view(), name="month_with_forms"),
    path('detail/<pk>', views.Detail.as_view(), name="detail"),
    path('update/<pk>', views.Update.as_view(), name="update"),
    path('delete/<pk>', views.Delete.as_view(), name="delete"),
    path('mypage/', mypage_site.urls),
]
