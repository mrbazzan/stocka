
from django.contrib.auth.backends import ModelBackend
from .models import UserAccount


class HashedPasswordAuthBackend(ModelBackend):

    def authenticate(self, request, email, password):
        try:
            user = UserAccount.objects.get(email=email, password=password)
        except UserAccount.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
