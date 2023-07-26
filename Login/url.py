from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='log_out'),
    path('phone_verification/', views.verify_phone_number, name='phone_verification'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('resend-code/', views.resend_code, name='resend_code'),
    path('change-number/', views.change_number, name='change_number'),
    ]
