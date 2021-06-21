from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
user = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = user
        fields = ('id', 'email', 'first', 'last_name', 'phone_number', 'password')