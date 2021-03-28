"""django_custom_auth_boilerplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from decouple import config


urlpatterns = [
    path('', include('accounts.urls')),

    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(config('ADMIN_URL'), admin.site.urls),

    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html', form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('activate/<uidb64>/<token>/',
         account_views.activate_account, name='activate'),
    path('account-activation-confirm', account_views.confirm_account,
         name='account_activation_confirm'),
]

if(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
