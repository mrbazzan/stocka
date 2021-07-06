
from django.contrib.auth import logout, authenticate
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer, PasswordResetSerializer
from .models import UserAccount


# Create your views here.


@api_view(["GET", ])
@permission_classes([IsAuthenticated, ])
def get_one_user_api_view(request, id):
    try:
        user = UserAccount.objects.get(id=id)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.is_admin:
        pass
    else:
        if str(user.email) != str(request.user):
            return Response(data={"message": "Permission required to view data"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data)


@api_view(["GET", ])
@permission_classes([IsAdminUser, ])
def get_all_user_api_view(request):
    try:
        users = UserAccount.objects.all()
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        response = []
        for user in users:
            serializer = UserRegistrationSerializer(user)
            response.append(serializer.data)
        return Response(response)


@swagger_auto_schema(method='post', request_body=UserRegistrationSerializer)
@permission_classes([AllowAny, ])
@api_view(["POST", ])
def register_user_api_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["response"] = "Succesfully registered a new user."
            data["id"] = user.id
            data["email"] = user.email
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            data["phone_number"] = user.phone_number
            data["business_name"] = user.business_name
            data["slug"] = user.slug
            token = Token.objects.get(user=user).key
            data["token"] = token
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['password', 'email or phone_number'],
            properties={
                'email or phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Email/Phone Number'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }),
        responses={200: TokenSerializer, 201: {}}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'token': token.key,
        })


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def log_out_view(request):
    logout(request)
    data = {"Response": "Successfully logged out"}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def authenticatedUser(request):
    
    if request.method == 'POST':
        data = {}
        try:
            key = Token.objects.get(key=request.data["token"])
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        authenticated_user = authenticate(request=request._request, email=key.user.email, password=key.user.password)

        if authenticated_user:
            data["id"] = authenticated_user.id
            data["First Name"] = authenticated_user.first_name
            data["Last Name"] = authenticated_user.last_name
            data["Email"] = authenticated_user.email
            data["Business Name"] = authenticated_user.business_name
            data["Phone Number"] = authenticated_user.phone_number
            return Response(data=data, status=status.HTTP_200_OK)

        data = {"Response": "User is not authenticated"}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def reset_password(request):

    user_email = request.data['email']

    try:
        user = UserAccount.objects.get(email=user_email)
    except UserAccount.DoesNotExist:
        return Response(
            data={'Response': "User with Email is not registered."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PasswordResetSerializer(data={"email": user_email})

    if serializer.is_valid():
        new_token = serializer.save()
        
        send_mail(
            "PASSWORD RESET",
            f"""You asked for password reset for user with email `{user_email}`.
            Copy this four(4) digit token: {new_token.token}
            
            Sincerely,
            Stocka Team.
            """,
            'zuristocka109@gmail.com',
            [user_email,],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)

    return Response(serializer.errors)
