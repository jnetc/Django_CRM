# Импорт шаблона начальной страницы из ./templates
from os import name
from leads.views import LandingPageView, SignupView
# Импорт шаблона авторизации пользователя ./templates/registration
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('reset-password/', PasswordResetView.as_view(), name="reset-password"),
    path('password-reset-done/', PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('password-reset-complete', PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

]
