from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_procuracao, name='cadastrar_procuracao'),
    path('api/buscar/', views.api_buscar_procuracoes, name='api_buscar_procuracoes'), # Nova URL
]