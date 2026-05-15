from decimal import Decimal
from rest_framework import serializers

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


# USUÁRIO
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        return Usuario.objects.create_user(**validated_data)


# CURSO
class CursoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(
        source="criado_por.username",
        read_only=True
    )

    class Meta:
        model = Curso
        fields = [
            "id",
            "nome",
            "descricao",
            "preco",
            "criado_por",
            "criado_por_nome",
            "total_vendas",
            "media_avaliacoes",
            "criacao",
        ]
        read_only_fields = [
            "id",
            "criado_por",
            "total_vendas",
            "media_avaliacoes",
            "criacao",
        ]


# AVALIAÇÃO (CORRIGIDO)
class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ["id", "usuario", "curso", "nota", "comentario", "criacao"]
        read_only_fields = ["id", "usuario", "criacao"]

    def validate(self, data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        curso = data.get("curso")

        qs = Avaliacao.objects.filter(
            usuario=request.user,
            curso=curso
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("Você já avaliou este curso")

        return data

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["usuario"] = request.user
        return Avaliacao.objects.create(**validated_data)


# COMPRA (CORRIGIDO)
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ["id", "usuario", "curso", "preco", "status"]
        read_only_fields = ["id", "usuario", "preco", "status"]

    def validate(self, data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        if not data.get("curso"):
            raise serializers.ValidationError("Curso obrigatório")

        return data

    def create(self, validated_data):
        request = self.context["request"]

        return Compra.objects.create(
            usuario=request.user,
            curso=validated_data["curso"]
        )


# AUDITORIA
class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = "__all__"