from abc import ABC

from .models import UserAccount
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'business_name', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = UserAccount(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            business_name=self.validated_data['business_name'],
            phone_number=self.validated_data['phone_number']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Password must match."})

        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.Serializer):

    token = serializers.CharField(
        label="Token",
        read_only=True
    )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="Email",
        write_only=True,
        required=False
    )

    phone_number = serializers.CharField(
        label="Phone Number",
        write_only=True,
        required=False
    )

    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        # This is to ensure a user can login with email or Phone Number
        # validate and authenticate user
        if email and password:

            # authenticate returns None if is_active=False users
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        elif phone_number and password:
            try:
                user_with_phone_num = UserAccount.objects.get(phone_number=phone_number)
            except UserAccount.DoesNotExist:
                raise serializers.ValidationError({"message": "Provide valid Phone number"})

            user = authenticate(request=self.context.get('request'),
                                email=user_with_phone_num.email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "Email/Phone Number" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
