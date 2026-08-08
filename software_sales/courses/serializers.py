from decimal import Decimal
from rest_framework import serializers

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


# USUÁRIO
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        return Usuario.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance


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

# AUDITORIA
class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = "__all__"
