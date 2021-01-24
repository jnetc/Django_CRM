from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path('', views.LeadListView.as_view(), name="lead-list"),
    path('<int:pk>/', views.LeadDetailView.as_view(), name="lead-detail"),
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name="lead-update"),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name="lead-delete"),
    path('create/', views.LeadCreateView.as_view(), name="lead-create"),
]
