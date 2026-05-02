from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Compra
from .serializers import CompraSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def perform_create(self, serializer):
        compra = serializer.save()

        email = compra.usuario.email
        curso = compra.curso.nome

        # simulando envio de email (sem Celery)
        print(f"Compra confirmada para {email} - curso: {curso}")
        print(f"Nota fiscal enviada para {email} - curso: {curso}")

    @action(detail=True, methods=["post"])
    def aprovar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.usuario.email
        curso = compra.curso.nome

        print(f"Reembolso aprovado: {email} - {curso}")

        return Response(
            {"message": "Reembolso aprovado e processado."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def recusar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.usuario.email
        curso = compra.curso.nome

        print(f"Reembolso recusado: {email} - {curso}")

        return Response(
            {"message": "Reembolso recusado."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def solicitar_reembolso(self, request, pk=None):
        compra = self.get_object()

        email = compra.usuario.email
        curso = compra.curso.nome

        print(f"Solicitação de reembolso: {email} - {curso}")

        return Response(
            {"message": "Solicitação de reembolso enviada."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def liberar_certificado(self, request, pk=None):
        compra = self.get_object()

        email = compra.usuario.email
        curso = compra.curso.nome

        print(f"Certificado liberado: {email} - {curso}")

        return Response(
            {"message": "Certificado liberado."},
            status=status.HTTP_200_OK
        )