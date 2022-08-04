from django.test import TestCase
from rest_framework.authtoken.models import Token

from .models import UserAccount, ResetPasswordTable


def get_token_count():
    return Token.objects.count()


class UserAccountTestCase(TestCase):
    def setUp(self):
        self.user_details = {
            "email": "luffy@gmail.com",
            "first_name": "Luffy",
            "last_name": "Monkey",
            "phone_number": "017",
            "business_name": "The luph",
            "password": "luffy",
        }
        # Create a user and superuser
        self.user = UserAccount.objects.create_superuser(
            email="test@superuser.com",
            first_name="Test",
            last_name="Normal User",
            phone_number="001",
            business_name="the-test",
            password="test"
        )
        self.superuser = UserAccount.objects.create_user(
            email="test@test.com",
            first_name="SuperTest",
            last_name="Super Test",
            phone_number="002",
            business_name="the-super",
            password="test"
        )

    def test_user_required_fields(self):
        with self.assertRaises(TypeError):
            UserAccount.objects.create_user(
                email="test_test@user.com"
            )

    def test_superuser_required_fields(self):
        with self.assertRaises(TypeError):
            UserAccount.objects.create_superuser(
                email="test_super@superuser.com"
            )

    def test_generate_slug(self):
        self.assertEqual(self.user.slug, "test-the-test")
        self.assertEqual(self.superuser.slug, "supertest-the-super")

    def test_token_generated_after_user_creation(self):
        # Test that token is generated with every User creation
        token_count = get_token_count()
        UserAccount.objects.create_user(**self.user_details)
        self.assertNotEqual(token_count, get_token_count())
