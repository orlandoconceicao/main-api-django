from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import (
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models


# BASE MODEL

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


# USER MANAGER

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email obrigatório")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, username, password, **extra_fields)


# USER CUSTOM

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


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
        on_delete=models.CASCADE,
        related_name="cursos"
    )

    total_vendas = models.PositiveIntegerField(default=0)

    media_avaliacoes = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00")
    )

    def __str__(self):
        return self.nome


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
        validators=[
            MinValueValidator(Decimal("1.00")),
            MaxValueValidator(Decimal("5.00")),
        ]
    )

    comentario = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(500)]
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.nome}"


# STATUS COMPRA

class CompraStatus(models.TextChoices):
    PENDING = "pending", "Pendente"
    PENDING_REFUND = "pending_refund", "Reembolso Pendente"
    COMPLETED = "completed", "Concluído"
    REFUNDED = "refunded", "Reembolsado"


# COMPRA

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
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=CompraStatus.choices,
        default=CompraStatus.PENDING
    )

    def save(self, *args, **kwargs):
        if self.preco is None:
            self.preco = self.curso.preco

        self.preco = Decimal(self.preco).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.nome}"


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

    acao = models.CharField(
        max_length=10,
        choices=ACAO_CHOICES
    )

    modelo = models.CharField(max_length=100)
    objeto_id = models.IntegerField()

    dados_antes = models.JSONField(
        null=True,
        blank=True
    )

    dados_depois = models.JSONField(
        null=True,
        blank=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]