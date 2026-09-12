from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Case


class CasePrivacyTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="safe-test-password")
        self.other_user = User.objects.create_user("other", password="safe-test-password")
        self.case = Case.objects.create(user=self.owner, title="Repair history", property_address="123 Main Street")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_owner_can_view_case(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.case.get_absolute_url()).status_code, 200)

    def test_other_user_cannot_view_case(self):
        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(self.case.get_absolute_url()).status_code, 404)

    def test_new_case_belongs_to_signed_in_user(self):
        self.client.force_login(self.owner)
        self.client.post(reverse("case_create"), {"title": "New case", "property_address": "456 Oak Avenue", "status": "active"})
        self.assertTrue(Case.objects.filter(user=self.owner, title="New case").exists())

# Create your tests here.
