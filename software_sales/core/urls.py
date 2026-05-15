from django.http import JsonResponse
from django.urls import path

def test(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", test),
]