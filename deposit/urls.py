# Trong file urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.deposit_view, name='deposit'),
    # Các URL khác cho chức năng nạp tiền nếu cần
]
