from django.urls import path
from .views import render_campanhas, api_campanhas_get, api_campanha_post, api_campanha_status_post

app_name = "vendas"  # Definição do app_name

urlpatterns = [
    path("campanhas/", render_campanhas, name="campanhas"),
    path("api/campanhas/", api_campanhas_get, name="api_campanhas_get"),
    path("api/campanha/", api_campanha_post, name="api_campanha_post"),
    path("api/campanha/status/", api_campanha_status_post, name="api_campanha_status_post"),
]
