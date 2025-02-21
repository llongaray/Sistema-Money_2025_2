from django.urls import path
from .views import dashboard

app_name = "ti"

urlpatterns = [
    path('', dashboard, name='dashboard_ti'),
]
