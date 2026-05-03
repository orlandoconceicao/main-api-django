from decimal import Decimal
from django.db.models import Avg

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

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


# CURSO
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.select_related("criado_por").all()
    serializer_class = CursoSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["criado_por"]

    permission_classes = [AllowAny]


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


    # ACTIONS


    @action(detail=True, methods=["post"])
    def solicitar_reembolso(self, request, pk=None):
        compra = self.get_object()

        if compra.status != CompraStatus.COMPLETED:
            return Response({"error": "Não permitido"}, status=400)

        compra.status = CompraStatus.PENDING_REFUND
        compra.save()

        return Response({"message": "Solicitação enviada"})

    @action(detail=True, methods=["post"])
    def aprovar_reembolso(self, request, pk=None):
        compra = self.get_object()

        compra.status = CompraStatus.REFUNDED
        compra.save()

        return Response({"message": "Reembolso aprovado"})

    @action(detail=True, methods=["post"])
    def recusar_reembolso(self, request, pk=None):
        compra = self.get_object()

        compra.status = CompraStatus.COMPLETED
        compra.save()

        return Response({"message": "Reembolso recusado"})

    @action(detail=True, methods=["post"])
    def liberar_certificado(self, request, pk=None):
        return Response({"message": "Certificado liberado"})