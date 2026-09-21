from django.urls import re_path
from .views import SignupView, LoginView, LogoutView, MeView, CustomTokenRefreshView

urlpatterns = [
    re_path(r'^signup/?$', SignupView.as_view(), name='auth_signup'),
    re_path(r'^login/?$', LoginView.as_view(), name='auth_login'),
    re_path(r'^logout/?$', LogoutView.as_view(), name='auth_logout'),
    re_path(r'^me/?$', MeView.as_view(), name='auth_me'),
    re_path(r'^refresh/?$', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
