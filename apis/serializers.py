
from abc import ABC

from django.contrib.auth import authenticate
from django.contrib.auth.models import BaseUserManager

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import UserAccount, ResetPasswordTable


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserAccount
        fields = ('token', 'id', 'email', 'first_name', 'last_name', 'phone_number', 'business_name', 'password', 'confirm_password')
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


class TokenSerializer(serializers.ModelSerializer):

    four_digit_token = serializers.CharField(
        write_only=True
    )

    token = serializers.SerializerMethodField()

    class Meta:
        model = ResetPasswordTable
        fields = ('four_digit_token', 'token')
        extra_kwargs = {"token": {"read_only": True}}
    
    def validate_four_digit_token(self, value):
        user = ResetPasswordTable.objects.filter(token=value)
        if not user:
            raise serializers.ValidationError({"Response": "Wrong Four Digit Token!"})

        return user.first()
    
    def get_token(self, obj):
        user_associated_with_token = UserAccount.objects.get(email=obj.get('four_digit_token').email)
        token = Token.objects.get(user_id=user_associated_with_token.id)
        return token.key


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


class ResetSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(label="Email", required=True, write_only=True)

    class Meta:
        model = ResetPasswordTable
        fields = ('email', 'token')
        extra_kwargs = {"token": {"read_only": True}}

    def validate_email(self, value):
        email_already_present = ResetPasswordTable.objects.filter(email=value)
        if email_already_present:
            email_already_present.delete()
        return BaseUserManager.normalize_email(value)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({'Password': "Password must match."})
        
        user = self.context['user']
        user.set_password(new_password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        user = self.context['user']
        if user.check_password(old_password):
            user.set_password(new_password)      
        else:
            raise serializers.ValidationError({'Response': "Enter Correct Old Password."})

        user.save()
        return user
