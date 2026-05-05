from decimal import Decimal
from django.db.models import Avg

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Compra,
    Curso,
    Usuario,
    Avaliacao,
    CompraStatus
)

from .serializers import (
    CompraSerializer,
    CursoSerializer,
    UsuarioSerializer,
    AvaliacaoSerializer
)


# USUARIO
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # usuário comum só vê ele mesmo
        if not self.request.user.is_staff:
            return Usuario.objects.filter(id=self.request.user.id)
        return Usuario.objects.all()


# CURSO
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.select_related("criado_por").all()
    serializer_class = CursoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["criado_por"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


# AVALIACAO
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.select_related("usuario", "curso").all()
    serializer_class = AvaliacaoSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        avaliacao = serializer.save(usuario=self.request.user)

        curso = avaliacao.curso

        media = curso.avaliacoes.aggregate(
            media=Avg("nota")
        )["media"] or Decimal("0.00")

        curso.media_avaliacoes = round(media, 2)
        curso.save()


# COMPRA
class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.select_related("usuario", "curso").all()
    serializer_class = CompraSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        compra = serializer.save(
            usuario=self.request.user,
            status=CompraStatus.COMPLETED
        )

        curso = compra.curso
        curso.total_vendas += 1
        curso.save()


    # REEMBOLSO - MAIS SEGURO
    @action(detail=True, methods=["post"])
    def solicitar_reembolso(self, request, pk=None):
        compra = self.get_object()

        if compra.usuario != request.user:
            return Response({"error": "Não permitido"}, status=403)

        if compra.status != CompraStatus.COMPLETED:
            return Response({"error": "Status inválido"}, status=400)

        compra.status = CompraStatus.PENDING_REFUND
        compra.save()

        return Response({"message": "Solicitação enviada"})


    # APROVAÇÃO (SÓ ADMIN)
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def aprovar_reembolso(self, request, pk=None):
        compra = self.get_object()

        compra.status = CompraStatus.REFUNDED
        compra.save()

        return Response({"message": "Reembolso aprovado"})


    # RECUSA (SÓ ADMIN)
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def recusar_reembolso(self, request, pk=None):
        compra = self.get_object()

        compra.status = CompraStatus.COMPLETED
        compra.save()

        return Response({"message": "Reembolso recusado"})


    @action(detail=True, methods=["post"])
    def liberar_certificado(self, request, pk=None):
        compra = self.get_object()

        if compra.usuario != request.user:
            return Response({"error": "Não permitido"}, status=403)

        return Response({"message": "Certificado liberado"})