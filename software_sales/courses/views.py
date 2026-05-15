from rest_framework import viewsets
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria
from .serializers import *


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer


class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer