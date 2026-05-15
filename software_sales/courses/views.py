from rest_framework import viewsets, permissions

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria
from .serializers import (
    UsuarioSerializer,
    CursoSerializer,
    AvaliacaoSerializer,
    CompraSerializer,
    AuditoriaSerializer,
)


# USUARIO
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]


# CURSO
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


# AVALIACAO
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# COMPRA
class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# AUDITORIA
class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer