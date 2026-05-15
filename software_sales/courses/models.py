from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models
from django.db.models import Avg


# BASE
class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


# USER
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username or "usuario"


# CURSO
class Curso(Base):
    nome = models.CharField(max_length=120)

    descricao = models.TextField(
        validators=[MaxLengthValidator(500)]
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("999.00")),
        ]
    )

    criado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cursos"
    )

    total_vendas = models.PositiveIntegerField(default=0)

    media_avaliacoes = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        editable=False
    )

    def atualizar_metricas(self):
        """Atualiza vendas e média com segurança."""
        self.total_vendas = self.compras.count()

        media = self.avaliacoes.aggregate(avg=Avg("nota")).get("avg")

        self.media_avaliacoes = (
            Decimal(str(media)).quantize(Decimal("0.01"), ROUND_HALF_UP)
            if media is not None else Decimal("0.00")
        )

        self.save(update_fields=["total_vendas", "media_avaliacoes"])

    def __str__(self):
        return self.nome or "curso"


# AVALIACAO
class Avaliacao(Base):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    nota = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comentario = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("usuario", "curso")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.curso_id:
            self.curso.atualizar_metricas()

    def delete(self, *args, **kwargs):
        curso = self.curso
        super().delete(*args, **kwargs)
        if curso:
            curso.atualizar_metricas()

    def __str__(self):
        return f"{self.usuario} → {self.curso}"


# COMPRA
class CompraStatus(models.TextChoices):
    PENDING = "pending", "Pendente"
    COMPLETED = "completed", "Concluído"
    REFUNDED = "refunded", "Reembolsado"


class Compra(Base):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="compras"
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="compras"
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    status = models.CharField(
        max_length=30,
        choices=CompraStatus.choices,
        default=CompraStatus.PENDING
    )

    def save(self, *args, **kwargs):
        if not self.preco:
            self.preco = self.curso.preco

        self.preco = Decimal(str(self.preco)).quantize(
            Decimal("0.01"),
            ROUND_HALF_UP
        )

        super().save(*args, **kwargs)

        if self.curso_id:
            self.curso.atualizar_metricas()

    def delete(self, *args, **kwargs):
        curso = self.curso
        super().delete(*args, **kwargs)
        if curso:
            curso.atualizar_metricas()

    def __str__(self):
        return f"{self.usuario} → {self.curso}"


# AUDITORIA
class Auditoria(models.Model):
    ACAO_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    acao = models.CharField(max_length=10, choices=ACAO_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.IntegerField()

    dados_antes = models.JSONField(null=True, blank=True)
    dados_depois = models.JSONField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.acao} - {self.modelo} ({self.objeto_id})"