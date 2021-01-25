# Импорт шаблона начальной страницы из ./templates
from os import name
from leads.views import LandingPageView, SignupView
# Импорт шаблона авторизации пользователя ./templates/registration
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]
