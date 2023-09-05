from django.contrib import admin
from django.urls import path
from users.views import registration, profile, others_profile
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', registration, name='blog_registration'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='blog_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='blog_logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', profile, name='blog_profile'),

    path('others_profile/<str:name>', others_profile, name='others_profile'),
]
