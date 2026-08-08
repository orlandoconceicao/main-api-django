from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Auditoria, Avaliacao, Compra, CompraStatus, Curso, Usuario


class ApiSecurityTests(APITestCase):
    def setUp(self):
        self.owner = Usuario.objects.create_user(
            username="owner", email="owner@example.com", password="strong-pass-1"
        )
        self.other = Usuario.objects.create_user(
            username="other", email="other@example.com", password="strong-pass-2"
        )
        self.course = Curso.objects.create(
            nome="Django",
            descricao="Curso de Django",
            preco=Decimal("100.00"),
            criado_por=self.owner,
        )

    def test_registration_hashes_password(self):
        response = self.client.post(
            reverse("usuario-list"),
            {"username": "new", "email": "NEW@example.com", "password": "strong-pass-3"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = Usuario.objects.get(username="new")
        self.assertTrue(user.check_password("strong-pass-3"))
        self.assertEqual(user.email, "new@example.com")

    def test_user_cannot_list_or_retrieve_other_users(self):
        self.client.force_authenticate(self.owner)
        response = self.client.get(reverse("usuario-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total"], 1)
        response = self.client.get(reverse("usuario-detail", args=[self.other.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_course_owner_can_modify_course(self):
        self.client.force_authenticate(self.other)
        response = self.client.patch(
            reverse("curso-detail", args=[self.course.pk]), {"nome": "Invadido"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_purchase_list_is_isolated_by_user(self):
        Compra.objects.create(usuario=self.owner, curso=self.course)
        Compra.objects.create(usuario=self.other, curso=self.course)
        self.client.force_authenticate(self.owner)
        response = self.client.get(reverse("compra-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total"], 1)
        self.assertEqual(response.data["data"][0]["usuario"], self.owner.pk)

    def test_audit_endpoint_requires_staff(self):
        self.client.force_authenticate(self.owner)
        response = self.client.get(reverse("auditoria-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_purchase_audit_records_authenticated_user(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(reverse("compra-list"), {"curso": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        audit = Auditoria.objects.get(modelo="Compra", objeto_id=response.data["id"])
        self.assertEqual(audit.usuario, self.owner)


class CourseMetricsTests(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="buyer", email="buyer@example.com", password="strong-pass-1"
        )
        self.course = Curso.objects.create(
            nome="Python", descricao="Curso de Python", preco=Decimal("50.00")
        )

    def test_only_completed_purchases_count_as_sales(self):
        purchase = Compra.objects.create(usuario=self.user, curso=self.course)
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_vendas, 0)
        purchase.status = CompraStatus.COMPLETED
        purchase.save(update_fields=["status"])
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_vendas, 1)
        purchase.status = CompraStatus.REFUNDED
        purchase.save(update_fields=["status"])
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_vendas, 0)

    def test_rating_average_updates_after_create_and_delete(self):
        rating = Avaliacao.objects.create(usuario=self.user, curso=self.course, nota=Decimal("4.50"))
        self.course.refresh_from_db()
        self.assertEqual(self.course.media_avaliacoes, Decimal("4.50"))
        rating.delete()
        self.course.refresh_from_db()
        self.assertEqual(self.course.media_avaliacoes, Decimal("0.00"))
