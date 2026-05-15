from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)

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

# SERVICES
from .services.compra_service import (
    criar_compra,
    solicitar_reembolso as solicitar_reembolso_service,
    aprovar_reembolso as aprovar_reembolso_service,
    recusar_reembolso as recusar_reembolso_service,
)

from .services.avaliacao_service import (
    criar_avaliacao,
)

# SELECTORS
from .selectors.compra_selector import (
    listar_compras_usuario,
)

from .selectors.curso_selector import (
    listar_cursos,
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
            return Usuario.objects.filter(
                id=self.request.user.id
            )

        return Usuario.objects.all()


# CURSO

class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = CursoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "criado_por",
        "ativo",
    ]

    search_fields = [
        "nome",
        "descricao",
    ]

    ordering_fields = [
        "preco",
        "criacao",
        "total_vendas",
        "media_avaliacoes",
    ]

    def get_queryset(self):
        return listar_cursos()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(
            criado_por=self.request.user
        )


# AVALIACAO

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.select_related(
        "usuario",
        "curso"
    ).all()

    serializer_class = AvaliacaoSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        criar_avaliacao(
            usuario=self.request.user,
            curso=serializer.validated_data["curso"],
            nota=serializer.validated_data["nota"],
            comentario=serializer.validated_data.get(
                "comentario",
                ""
            )
        )


# COMPRA

class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = CompraSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return listar_compras_usuario(
            self.request.user
        )

    def perform_create(self, serializer):
        criar_compra(
            usuario=self.request.user,
            curso=serializer.validated_data["curso"]
        )

    # =====================================================
    # SOLICITAR REEMBOLSO
    # =====================================================

    @action(detail=True, methods=["post"])
    def solicitar_reembolso(self, request, pk=None):
        compra = self.get_object()

        if compra.usuario != request.user:
            return Response(
                {"error": "Não permitido"},
                status=403
            )

        if compra.status != CompraStatus.COMPLETED:
            return Response(
                {"error": "Status inválido"},
                status=400
            )

        solicitar_reembolso_service(
            compra=compra
        )

        return Response({
            "message": "Solicitação enviada"
        })

    # =====================================================
    # APROVAR REEMBOLSO
    # =====================================================

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser]
    )
    def aprovar_reembolso(self, request, pk=None):
        compra = self.get_object()

        aprovar_reembolso_service(
            compra=compra
        )

        return Response({
            "message": "Reembolso aprovado"
        })

    # =====================================================
    # RECUSAR REEMBOLSO
    # =====================================================

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser]
    )
    def recusar_reembolso(self, request, pk=None):
        compra = self.get_object()

        recusar_reembolso_service(
            compra=compra
        )

        return Response({
            "message": "Reembolso recusado"
        })

    # =====================================================
    # CERTIFICADO
    # =====================================================

    @action(detail=True, methods=["post"])
    def liberar_certificado(self, request, pk=None):
        compra = self.get_object()

        if compra.usuario != request.user:
            return Response(
                {"error": "Não permitido"},
                status=403
            )

        return Response({
            "message": "Certificado liberado"
        })