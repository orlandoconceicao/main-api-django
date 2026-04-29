from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Purchase
from .serializers import PurchaseSerializer

from .tasks import (
    enviar_email_boas_vindas,
    enviar_email_compra,
    processar_reembolso,
    enviar_email_recuperacao_senha,
    enviar_email_verificacao,
    enviar_email_compra_recusada,
    enviar_email_certificado,
    enviar_email_nota_fiscal,
    enviar_email_reembolso_aprovado,
    enviar_email_reembolso_recusado,
    enviar_relatorio_diario,
)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        compra = serializer.save()

        email = compra.user.email
        curso = compra.course.title

        enviar_email_compra(email, curso)
        enviar_email_nota_fiscal(email, curso)

    @action(detail=True, methods=["post"])
    def aprovar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.user.email
        curso = compra.course.title

        enviar_email_reembolso_aprovado(email, curso)

        return Response(
            {"message": "Reembolso aprovado e e-mail enviado."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def recusar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.user.email
        curso = compra.course.title

        enviar_email_reembolso_recusado(email, curso)

        return Response(
            {"message": "Reembolso recusado e e-mail enviado."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def solicitar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.user.email
        curso = compra.course.title

        processar_reembolso(email, curso)

        return Response(
            {"message": "Solicitação de reembolso enviada."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def liberar_certificado(self, request, pk=None):
        compra = self.get_object()

        email = compra.user.email
        curso = compra.course.title

        enviar_email_certificado(email, curso)

        return Response(
            {"message": "Certificado liberado e e-mail enviado."},
            status=status.HTTP_200_OK
        )