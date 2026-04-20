from rest_framework import serializers
from decimal import Decimal
from .models import Usuario, Curso, Avaliacao, Compra, CompraStatus


# Serializer => Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    # Senha so para escrita, não retorna na API
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        # Campo exposto
        fields = ['id', 'email', 'username', 'password', 'criacao']
        # Campos controlado pelo backend
        read_only_fields = ['id', 'criacao']

    def create(self, validated_data):
        # Cria usuario com senha criptografada
        return Usuario.objects.create_user(**validated_data)

    def validate_email(self, value):
        # Normaliza email
        value = value.lower()

        # Garante email unico (evita erro 500)
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já está em uso")

        return value

    def validate_username(self, value):
        # Valida tamanho minimo
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username deve ter no mínimo 3 caracteres"
            )
        return value


# Serializer => Curso
class CursoSerializer(serializers.ModelSerializer):
    # Nome do criador (campo relacionado)
    criado_por_nome = serializers.CharField(
        source='criado_por.username',
        read_only=True
    )

    # Campo calculado (usar annotate view)
    total_avaliacoes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Curso
        fields = [
            'id',
            'nome',
            'descricao',
            'preco',
            'criado_por',
            'criado_por_nome',
            'total_vendas',
            'total_avaliacoes',
            'criacao'
        ]

        # Impede manipulação de dados sensíveis
        read_only_fields = [
            'id',
            'total_vendas',
            'criacao',
            'criado_por'
        ]

    def validate_nome(self, value):
        # Nome minimo
        if len(value) < 3:
            raise serializers.ValidationError(
                "Nome deve ter no mínimo 3 caracteres"
            )
        return value

    def validate_descricao(self, value):
        # Descrição minima
        if len(value) < 10:
            raise serializers.ValidationError(
                "Descrição deve ter no mínimo 10 caracteres"
            )
        return value

    def validate_preco(self, value):
        # Valida preço mínimo
        if value < Decimal('0.00'):
            raise serializers.ValidationError(
                "Preço não pode ser negativo"
            )

        # Valida preço máximo
        if value > Decimal('999.00'):
            raise serializers.ValidationError(
                "Preço máximo permitido é R$ 999,00"
            )

        return value

    def validate(self, data):
        # Regra de negócio global
        nome = data.get("nome")
        descricao = data.get("descricao")

        # Evita descrição ruim
        if nome and descricao and nome in descricao:
            raise serializers.ValidationError(
                "A descrição não pode conter o mesmo nome do curso"
            )

        return data

    def create(self, validated_data):
        # Define automaticamente o criador
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Usuário não identificado"
            )

        validated_data['criado_por'] = request.user
        return super().create(validated_data)


# Serializer => Avaliacao
class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliacao
        fields = [
            'id',
            'usuario',
            'curso',
            'nota',
            'comentario',
            'criacao'
        ]

        # Usuario vem de backend
        read_only_fields = [
            'id',
            'criacao',
            'usuario'
        ]

    def validate_nota(self, value):
        # Garante nota de 1 a 5
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Nota deve estar entre 1 e 5"
            )
        return value

    def validate_comentario(self, value):
        # Evita comentario lixo
        if value and len(value) < 3:
            raise serializers.ValidationError(
                "Comentário deve ter no mínimo 3 caracteres"
            )
        return value

    def validate(self, data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Usuário não identificado"
            )

        usuario = request.user
        curso = data.get('curso') or getattr(
            self.instance,
            'curso',
            None
        )

        # Curso obrigatório
        if not curso:
            raise serializers.ValidationError(
                "Curso é obrigatório"
            )

        # Verifica se comprou
        if not Compra.objects.filter(
            usuario=usuario,
            curso=curso,
            status=CompraStatus.COMPLETED
        ).exists():
            raise serializers.ValidationError(
                "É necessário comprar o curso antes de enviar uma avaliação"
            )

        # Impede duplicidade (create/update)
        if Avaliacao.objects.filter(
            usuario=usuario,
            curso=curso
        ).exclude(
            id=self.instance.id if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                "Você já avaliou este curso"
            )

        # Define usuario automaticamente
        data['usuario'] = usuario
        return data


# Serializer => Compra
class CompraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compra
        fields = [
            'id',
            'usuario',
            'curso',
            'preco',
            'status'
        ]

        # Campos sensiveis controlados por backend
        read_only_fields = [
            'id',
            'usuario',
            'preco',
            'status'
        ]

    def validate(self, data):
        request = self.context.get('request')

        # Garante usuario autenticado
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Usuário precisa estar autenticado"
            )

        usuario = request.user
        curso = data.get('curso')

        # Curso obrigatório
        if not curso:
            raise serializers.ValidationError(
                "Curso é obrigatório"
            )

        # Impede compra duplicada
        if Compra.objects.filter(
            usuario=usuario,
            curso=curso
        ).exists():
            raise serializers.ValidationError(
                "Este curso já foi comprado por você"
            )

        # Impede comprar próprio curso
        if curso.criado_por == usuario:
            raise serializers.ValidationError(
                "Não é permitido comprar seu próprio curso"
            )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        usuario = request.user
        curso = validated_data['curso']

        # Cria compra com dados seguros
        return Compra.objects.create(
            usuario=usuario,
            curso=curso,
            preco=curso.preco
        )


# Serializer => CompraStatus (choices)
class CompraStatusSerializer(serializers.Serializer):
    # Retorna todos os status disponiveis
    status = serializers.ChoiceField(
        choices=CompraStatus.choices
    )


# Serializer => Histórico
class HistoricoSerializer(serializers.Serializer):
    # Tipo do evento (compra, avaliacao, reembolso)
    tipo = serializers.CharField()

    # Nome do curso
    curso = serializers.CharField()

    # Nota (opcional)
    nota = serializers.FloatField(required=False)

    # Preço (opcional)
    preco = serializers.CharField(required=False)

    # Status (opcional)
    status = serializers.CharField(required=False)

    # Data do evento
    data = serializers.DateTimeField()