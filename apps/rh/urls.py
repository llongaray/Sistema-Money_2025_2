from django.urls import path
from .views import *

app_name = "rh"

urlpatterns = [
    # ========== RENDERIZAÇÃO ==========
    path('categorias/', render_categorias, name='render_categorias'),
    path('funcionarios/', render_funcionarios, name='render_funcionarios'),
    path('usuarios/', render_usuarios, name='render_usuarios'),
    path('arquivos-funcionario/', render_arquivos_funcionario, name='render_arquivos_funcionario'),
    path('funcionarios/editar/', render_edit_funcionario, name='render_edit_funcionario'),

    # ========== API GET ==========
    path('api/get/', api_rh_get, name='api_rh_get'),

    # ========== API POST ==========
    path('api/empresa/', api_empresa_post, name='api_empresa_post'),
    path('api/hierarquia/', api_hierarquia_post, name='api_hierarquia_post'),
    path('api/departamento/', api_departamento_post, name='api_departamento_post'),
    path('api/equipe/', api_equipe_post, name='api_equipe_post'),
    path('api/cargo/', api_cargo_post, name='api_cargo_post'),
    path('api/loja/', api_loja_post, name='api_loja_post'),
    path('api/horario/', api_horario_post, name='api_horario_post'),
    path('api/funcionario/', api_funcionario_post, name='api_funcionario_post'),
    path('api/usuario/', api_usuario_post, name='api_usuario_post'),
    path('api/arquivos-funcionario/', api_arquivos_funcionario_post, name='api_arquivos_funcionario_post'),
    path('api/funcionario/editar/', api_funcionario_edit_post, name='api_funcionario_edit_post'),
]
