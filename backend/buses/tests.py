from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from buses.models import Bus

User = get_user_model()


class BusAPITests(APITestCase):
    def setUp(self):
        self.authority = User.objects.create_user(
            email="auth@test.com", password="StrongPass!123", role="authority"
        )
        self.passenger = User.objects.create_user(
            email="p@test.com", password="StrongPass!123", role="passenger"
        )
        self.bus = Bus.objects.create(bus_number="MH13-100", license_plate="MH13-XX-0001")

    def test_passenger_can_list_buses(self):
        self.client.force_authenticate(user=self.passenger)
        r = self.client.get("/api/buses/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_passenger_cannot_create_bus(self):
        self.client.force_authenticate(user=self.passenger)
        payload = {"bus_number": "MH13-200", "license_plate": "MH13-YY-0002", "capacity": 40}
        r = self.client.post("/api/buses/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_authority_can_create_bus(self):
        self.client.force_authenticate(user=self.authority)
        payload = {"bus_number": "MH13-200", "license_plate": "MH13-YY-0002", "capacity": 40}
        r = self.client.post("/api/buses/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Bus.objects.filter(bus_number="MH13-200").exists())

    def test_duplicate_bus_number_rejected(self):
        self.client.force_authenticate(user=self.authority)
        payload = {"bus_number": "MH13-100", "license_plate": "MH13-ZZ-0003", "capacity": 40}
        r = self.client.post("/api/buses/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access_denied(self):
        r = self.client.get("/api/buses/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)