from leads.views import LandingPageView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path('leads/', include('leads.urls', namespace="leads")),
]
