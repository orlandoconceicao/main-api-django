from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria
from .serializers import (
    UsuarioSerializer,
    CursoSerializer,
    AvaliacaoSerializer,
    CompraSerializer,
    AuditoriaSerializer,
)

PAGINATION_PARAMETERS = [
    openapi.Parameter(
        "page",
        openapi.IN_QUERY,
        description="Página de resultados para paginação.",
        type=openapi.TYPE_INTEGER,
        example=1,
    ),
    openapi.Parameter(
        "page_size",
        openapi.IN_QUERY,
        description="Número de itens por página.",
        type=openapi.TYPE_INTEGER,
        example=10,
    ),
]

SEARCH_PARAMETER = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Busca por texto nos campos configurados do endpoint.",
    type=openapi.TYPE_STRING,
    example="python",
)

ORDERING_PARAMETER = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="Ordenação de resultados. Prefixe com '-' para ordem decrescente.",
    type=openapi.TYPE_STRING,
    example="-criacao",
)

PRICE_FILTER_PARAMETERS = [
    openapi.Parameter(
        "preco__gte",
        openapi.IN_QUERY,
        description="Filtrar cursos ou compras com preço maior ou igual.",
        type=openapi.TYPE_NUMBER,
        example=100.00,
    ),
    openapi.Parameter(
        "preco__lte",
        openapi.IN_QUERY,
        description="Filtrar cursos ou compras com preço menor ou igual.",
        type=openapi.TYPE_NUMBER,
        example=500.00,
    ),
]

STATUS_FILTER_PARAMETER = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="Filtrar compras por status (pending, completed, refunded).",
    type=openapi.TYPE_STRING,
    example="completed",
)

COURSE_FILTER_PARAMETER = openapi.Parameter(
    "curso",
    openapi.IN_QUERY,
    description="Filtrar avaliações e compras pelo ID do curso.",
    type=openapi.TYPE_INTEGER,
    example=1,
)

USER_FILTER_PARAMETER = openapi.Parameter(
    "usuario",
    openapi.IN_QUERY,
    description="Filtrar avaliações e compras pelo ID do usuário.",
    type=openapi.TYPE_INTEGER,
    example=1,
)

AUDIT_FILTER_PARAMETERS = [
    openapi.Parameter(
        "modelo",
        openapi.IN_QUERY,
        description="Filtrar auditoria por nome do modelo.",
        type=openapi.TYPE_STRING,
        example="Curso",
    ),
    openapi.Parameter(
        "acao",
        openapi.IN_QUERY,
        description="Filtrar auditoria por tipo de ação (CREATE, UPDATE, DELETE).",
        type=openapi.TYPE_STRING,
        example="CREATE",
    ),
]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Listar usuários",
        operation_description=(
            "Retorna uma lista de usuários. Use search para filtrar por username ou email, "
            "page/page_size para paginação e ordering para ordenação."
        ),
        tags=["Auth"],
        operation_id="listarUsuarios",
        manual_parameters=PAGINATION_PARAMETERS + [SEARCH_PARAMETER, ORDERING_PARAMETER],
        responses={
            200: openapi.Response(
                description="Lista de usuários retornada com sucesso",
                schema=UsuarioSerializer(many=True),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Detalhar usuário",
        operation_description="Retorna os dados de um usuário específico pelo ID.",
        tags=["Auth"],
        operation_id="detalharUsuario",
        responses={
            200: openapi.Response(
                description="Usuário retornado com sucesso",
                schema=UsuarioSerializer(),
            ),
            404: openapi.Response(description="Usuário não encontrado"),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Criar usuário",
        operation_description=(
            "Cria um novo usuário. O campo password é escrito apenas no momento da criação."
        ),
        tags=["Auth"],
        operation_id="criarUsuario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="orlando"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, example="orlando@example.com"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, example="Admin@123"),
            },
            required=["username", "email", "password"],
        ),
        responses={
            201: openapi.Response(
                description="Usuário criado com sucesso",
                schema=UsuarioSerializer(),
            ),
            400: openapi.Response(description="Dados inválidos"),
        },
    ),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["username", "email"]
    ordering_fields = ["username", "email", "id"]
    ordering = ["username"]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Listar cursos",
        operation_description=(
            "Retorna cursos com filtros por preço, busca por texto e ordenação. "
            "Use page/page_size para controlar paginação."
        ),
        tags=["Cursos"],
        operation_id="listarCursos",
        manual_parameters=PAGINATION_PARAMETERS + [SEARCH_PARAMETER, ORDERING_PARAMETER] + PRICE_FILTER_PARAMETERS,
        responses={
            200: openapi.Response(
                description="Lista de cursos retornada com sucesso",
                schema=CursoSerializer(many=True),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Detalhar curso",
        operation_description="Retorna informações completas de um curso, incluindo métricas e autor.",
        tags=["Cursos"],
        operation_id="detalharCurso",
        responses={
            200: openapi.Response(
                description="Curso detalhado retornado com sucesso",
                schema=CursoSerializer(),
            ),
            404: openapi.Response(description="Curso não encontrado"),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Criar curso",
        operation_description=(
            "Cria um novo curso. Requer autenticação JWT e atribui o curso ao usuário logado."
        ),
        tags=["Cursos"],
        operation_id="criarCurso",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "nome": openapi.Schema(type=openapi.TYPE_STRING, example="Python Full Stack"),
                "descricao": openapi.Schema(type=openapi.TYPE_STRING, example="Curso completo com Python, Django REST e boas práticas."),
                "preco": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=297.00),
            },
            required=["nome", "descricao", "preco"],
        ),
        responses={
            201: openapi.Response(
                description="Curso criado com sucesso",
                schema=CursoSerializer(),
            ),
            400: openapi.Response(description="Dados inválidos"),
            401: openapi.Response(description="Autenticação necessária"),
        },
    ),
)
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["nome", "descricao"]
    ordering_fields = ["preco", "criacao", "total_vendas", "media_avaliacoes"]
    filterset_fields = {"preco": ["gte", "lte"]}
    ordering = ["nome"]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(criado_por=self.request.user)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Listar avaliações",
        operation_description=(
            "Retorna avaliações de cursos. Filtre por curso, nota e texto do comentário."
        ),
        tags=["Avaliações"],
        operation_id="listarAvaliacoes",
        manual_parameters=PAGINATION_PARAMETERS + [SEARCH_PARAMETER, ORDERING_PARAMETER, COURSE_FILTER_PARAMETER, USER_FILTER_PARAMETER],
        responses={
            200: openapi.Response(
                description="Lista de avaliações retornada com sucesso",
                schema=AvaliacaoSerializer(many=True),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Detalhar avaliação",
        operation_description="Retorna os dados completos de uma avaliação específica.",
        tags=["Avaliações"],
        operation_id="detalharAvaliacao",
        responses={
            200: openapi.Response(
                description="Avaliação retornada com sucesso",
                schema=AvaliacaoSerializer(),
            ),
            404: openapi.Response(description="Avaliação não encontrada"),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Criar avaliação",
        operation_description=(
            "Cria uma avaliação para um curso. O usuário autenticado será registrado como autor. "
            "Nota deve estar entre 1 e 5."
        ),
        tags=["Avaliações"],
        operation_id="criarAvaliacao",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "curso": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "nota": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=4.5),
                "comentario": openapi.Schema(type=openapi.TYPE_STRING, example="Conteúdo muito relevante e didático."),
            },
            required=["curso", "nota"],
        ),
        responses={
            201: openapi.Response(
                description="Avaliação criada",
                schema=AvaliacaoSerializer(),
            ),
            400: openapi.Response(description="Dados inválidos"),
            401: openapi.Response(description="Autenticação necessária"),
        },
    ),
)
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["comentario", "curso__nome", "usuario__username"]
    ordering_fields = ["nota", "criacao"]
    filterset_fields = {"nota": ["gte", "lte"], "curso": ["exact"], "usuario": ["exact"]}
    ordering = ["-criacao"]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(usuario=self.request.user)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Listar compras",
        operation_description=(
            "Retorna o histórico de compras. Use search, status, curso, usuario e ordering para filtrar e ordenar os resultados."
        ),
        tags=["Compras"],
        operation_id="listarCompras",
        manual_parameters=PAGINATION_PARAMETERS + [SEARCH_PARAMETER, ORDERING_PARAMETER, STATUS_FILTER_PARAMETER, COURSE_FILTER_PARAMETER, USER_FILTER_PARAMETER] + PRICE_FILTER_PARAMETERS,
        responses={
            200: openapi.Response(
                description="Lista de compras retornada com sucesso",
                schema=CompraSerializer(many=True),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Detalhar compra",
        operation_description="Retorna as informações de uma compra específica, incluindo status e preço.",
        tags=["Compras"],
        operation_id="detalharCompra",
        responses={
            200: openapi.Response(
                description="Compra retornada com sucesso",
                schema=CompraSerializer(),
            ),
            404: openapi.Response(description="Compra não encontrada"),
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Criar compra",
        operation_description=(
            "Cria uma compra simbólica para demonstração do fluxo de checkout. "
            "O preço do curso é preenchido automaticamente e o status inicial é pending."
        ),
        tags=["Compras"],
        operation_id="criarCompra",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "curso": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            },
            required=["curso"],
        ),
        responses={
            201: openapi.Response(
                description="Compra criada com status pending",
                schema=CompraSerializer(),
            ),
            400: openapi.Response(description="Dados inválidos"),
            401: openapi.Response(description="Autenticação necessária"),
        },
    ),
)
class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["curso__nome", "usuario__username", "status"]
    ordering_fields = ["preco", "criacao"]
    filterset_fields = {"preco": ["gte", "lte"], "status": ["exact"], "curso": ["exact"]}
    ordering = ["-criacao"]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Login obrigatório")

        serializer.save(usuario=self.request.user)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Listar registros de auditoria",
        operation_description=(
            "Retorna o histórico de auditoria com ações de criação, atualização e exclusão."
        ),
        tags=["Admin"],
        operation_id="listarAuditoria",
        manual_parameters=PAGINATION_PARAMETERS + [SEARCH_PARAMETER, ORDERING_PARAMETER] + AUDIT_FILTER_PARAMETERS,
        responses={
            200: openapi.Response(
                description="Lista de auditoria retornada com sucesso",
                schema=AuditoriaSerializer(many=True),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Detalhar auditoria",
        operation_description="Mostra os dados antes e depois de uma ação registrada no sistema.",
        tags=["Admin"],
        operation_id="detalharAuditoria",
        responses={
            200: openapi.Response(
                description="Registro de auditoria retornado com sucesso",
                schema=AuditoriaSerializer(),
            ),
            404: openapi.Response(description="Registro de auditoria não encontrado"),
        },
    ),
)
class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["usuario__username", "modelo", "acao"]
    ordering_fields = ["criado_em"]
    ordering = ["-criado_em"]
