from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AccountTests(APITestCase):
    def test_create_custom_user(self):
        url = reverse("user_register")
        data = {
            "email": "kaido@gmail.com",
            "first_name": "Luffy",
            "last_name": "Monkey",
            "phone_number": "017",
            "business_name": "The luph"
        }
        password_data = {
            "password": "luffy",
            "confirm_password": "luffy"
        }
        response = self.client.post(url, {**data, **password_data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = Token.objects.get(user__email=data["email"]).key
        self.assertEqual(response.data["token"], token)
        self.assertEqual(response.data["email"], data["email"])

    def test_create_custom_user_no_required_fields(self):
        """
        Test what happens when the required fields are not passed
        """
        url = reverse("user_register")
        data = {
            "email": "kaido@gmail.com",
            "first_name": "Luffy",
            "last_name": "Monkey",
            "phone_number": "017"
        }
        password_data = {
            "password": "luffy",
            "confirm_password": "luffy"
        }
        response = self.client.post(url, {**data, **password_data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("business_name", response.data)
