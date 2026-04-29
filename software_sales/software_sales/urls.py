from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from courses.urls import public_router, admin_router


# ROTA PRINCIPAL (HOME DA API)
def home(request):
    return JsonResponse({
        "status": "API rodando 🚀",
        "docs": "/swagger/",
        "admin": "/admin/",
        "api": "/api/"
    })


urlpatterns = [
    # HOME
    path('', home),

    # ADMIN DJANGO
    path('admin/', admin.site.urls),

    # API (ROTAS DO APP)
    path('api/', include(public_router.urls)),
    path('api/admin/', include(admin_router.urls)),
]