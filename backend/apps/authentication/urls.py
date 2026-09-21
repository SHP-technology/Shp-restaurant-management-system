from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, LoginView, LogoutView, MeView

urlpatterns = [
    re_path(r'^signup/?$', SignupView.as_view(), name='auth_signup'),
    re_path(r'^login/?$', LoginView.as_view(), name='auth_login'),
    re_path(r'^logout/?$', LogoutView.as_view(), name='auth_logout'),
    re_path(r'^me/?$', MeView.as_view(), name='auth_me'),
    re_path(r'^refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
]
