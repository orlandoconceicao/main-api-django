from decimal import Decimal

from rest_framework import serializers

from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


# USUARIO
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "email", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        return Usuario.objects.create_user(**validated_data)

    def validate_email(self, value):
        value = value.lower()

        qs = Usuario.objects.filter(email=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("Email já está em uso")

        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username muito curto")
        return value


# CURSO
class CursoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source="criado_por.username", read_only=True)

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

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Nome muito curto")
        return value

    def validate_descricao(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Descrição muito curta")
        return value

    def validate_preco(self, value):
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Preço inválido")
        return value


# AVALIACAO
class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ["id", "usuario", "curso", "nota", "comentario", "criacao"]
        read_only_fields = ["id", "usuario", "criacao"]

    def validate(self, data):
        request = self.context.get("request")

        if request and request.user and data.get("curso"):
            qs = Avaliacao.objects.filter(
                usuario=request.user,
                curso=data["curso"]
            )

            if self.instance:
                qs = qs.exclude(id=self.instance.id)

            if qs.exists():
                raise serializers.ValidationError("Você já avaliou este curso")

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["usuario"] = request.user
        return super().create(validated_data)


# COMPRA
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ["id", "usuario", "curso", "preco", "status"]
        read_only_fields = ["id", "usuario", "preco", "status"]

    def create(self, validated_data):
        request = self.context.get("request")

        return Compra.objects.create(
            usuario=request.user,
            curso=validated_data["curso"]
        )


# AUDITORIA
class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = "__all__"