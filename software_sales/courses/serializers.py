from decimal import Decimal

from rest_framework import serializers
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        return Usuario.objects.create_user(**validated_data)


class CursoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source="criado_por.username", read_only=True)

    class Meta:
        model = Curso
        fields = "__all__"
        read_only_fields = ["total_vendas", "media_avaliacoes"]


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = "__all__"
        read_only_fields = ["usuario"]

    def create(self, validated_data):
        validated_data["usuario"] = self.context["request"].user
        return super().create(validated_data)


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = "__all__"
        read_only_fields = ["usuario", "preco", "status"]

    def create(self, validated_data):
        validated_data["usuario"] = self.context["request"].user
        return super().create(validated_data)


class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = "__all__"