from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthFlowTests(APITestCase):
    def test_register_passenger(self):
        url = reverse("users:register")
        payload = {
            "email": "p1@test.com",
            "full_name": "Passenger One",
            "role": "passenger",
            "password": "StrongPass!123",
            "password_confirm": "StrongPass!123",
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="p1@test.com").exists())

    def test_register_rejects_authority_role(self):
        url = reverse("users:register")
        payload = {
            "email": "a1@test.com",
            "role": "authority",
            "password": "StrongPass!123",
            "password_confirm": "StrongPass!123",
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens_and_user(self):
        User.objects.create_user(
            email="d1@test.com", password="StrongPass!123", role="driver"
        )
        url = reverse("users:login")
        r = self.client.post(
            url, {"email": "d1@test.com", "password": "StrongPass!123"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertEqual(r.data["user"]["role"], "driver")

    def test_profile_requires_auth(self):
        url = reverse("users:profile")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_returns_current_user(self):
        user = User.objects.create_user(
            email="me@test.com", password="StrongPass!123", role="passenger"
        )
        self.client.force_authenticate(user=user)
        url = reverse("users:profile")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["data"]["email"], "me@test.com")