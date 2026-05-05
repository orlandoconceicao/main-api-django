from decimal import Decimal

from rest_framework import serializers

from .models import (
    Usuario,
    Curso,
    Avaliacao,
    Compra,
)


# USUARIO
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "username",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)

    def validate_email(self, value):
        value = value.lower()

        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já está em uso")

        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username deve ter no mínimo 3 caracteres"
            )
        return value


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
            "total_vendas",
            "media_avaliacoes",
            "criacao",
            "criado_por",
        ]

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Nome deve ter no mínimo 3 caracteres"
            )
        return value

    def validate_descricao(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Descrição deve ter no mínimo 10 caracteres"
            )
        return value

    def validate_preco(self, value):
        if value < Decimal("0.00"):
            raise serializers.ValidationError(
                "Preço não pode ser negativo"
            )
        return value


# AVALIACAO
class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = [
            "id",
            "usuario",
            "curso",
            "nota",
            "comentario",
            "criacao",
        ]

        read_only_fields = [
            "id",
            "criacao",
            "usuario",
        ]

    def validate(self, data):
        request = self.context.get("request")
        curso = data.get("curso")

        # impede avaliação duplicada
        if request and curso:
            if Avaliacao.objects.filter(
                usuario=request.user,
                curso=curso
            ).exists():
                raise serializers.ValidationError(
                    "Você já avaliou este curso"
                )

        return data


# COMPRA
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = [
            "id",
            "usuario",
            "curso",
            "preco",
            "status",
        ]

        read_only_fields = [
            "id",
            "usuario",
            "preco",
            "status",
        ]

    def validate(self, data):
        curso = data.get("curso")

        if not curso:
            raise serializers.ValidationError("Curso inválido")

        return data

    def create(self, validated_data):
        request = self.context.get("request")

        return Compra.objects.create(
            usuario=request.user,
            curso=validated_data["curso"],
            preco=validated_data["curso"].preco
        )


# HISTORICO (SEGURANÇA MELHORADA)
class HistoricoSerializer(serializers.Serializer):
    tipo = serializers.CharField(read_only=True)
    curso = serializers.CharField(read_only=True)
    nota = serializers.FloatField(required=False, read_only=True)
    preco = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    data = serializers.DateTimeField(read_only=True)