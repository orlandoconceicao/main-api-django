from rest_framework import viewsets, permissions

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria
from .serializers import (
    UsuarioSerializer,
    CursoSerializer,
    AvaliacaoSerializer,
    CompraSerializer,
    AuditoriaSerializer,
)


# USUÁRIO
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]


# CURSO
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(criado_por=self.request.user)


# AVALIAÇÃO
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(usuario=self.request.user)


# COMPRA
class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(usuario=self.request.user)


# AUDITORIA
class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer