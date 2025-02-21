from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('diretoria/', include('apps.diretoria.urls')),
    # path('inss/', include('apps.inss.urls')),
    # path('mkt/', include('apps.mkt.urls')),
    # path('rankings/', include('apps.rankings.urls')),
    path('rh/', include('apps.rh.urls')),
    # path('siape/', include('apps.siape.urls')),
    path('', include('apps.ti.urls')),
    path('autenticacao/', include('apps.usuarios.urls')),
    path('vendas/', include('apps.vendas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
