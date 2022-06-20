from time import time
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.utils import json
from rest_framework_simplejwt.tokens import RefreshToken
from ecommerce.common.emails import send_email_without_delay
from user import models as user_models
import jwt
from django.template.loader import render_to_string
from user import serializers as user_serializers
from user.models import CustomerProfile, User
from rest_framework.views import APIView
from user.serializers import CustomerProfileUpdateSerializer, SubscriptionSerializer


class RegisterUser(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = user_models.User.objects.all()
    serializer_class = user_serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = user_serializers.UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = user_models.User.objects.none()
            try:
                user = user_models.User.objects.get(
                    email=request.data["email"])

                token = RefreshToken.for_user(user)

                exp = time() + 1200 #20 minutes
                email_list = request.data["email"]
                subject = "Verify Your Account"
                token = jwt.encode({'email': email_list, 'exp': exp, 'scope': subject},
                                   settings.JWT_SECRET, algorithm='HS256')
                html_message = render_to_string('verification_email.html', {'token': token, 'domain': settings.EMAIL_DOMAIN_NAME})
                send_email_without_delay(subject, html_message, email_list)
                CustomerProfile.objects.create(user=user)
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "full_name": user.first_name + " " + user.last_name
                }
                return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
            except (user_models.User.DoesNotExist):
                if user:
                    user.delete()
                return Response({"status": False, "data": {"message": "User not registered. Please try again."}}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": False, "data": {"message": "User not registered. Please try again.", "errors": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginUser(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = user_serializers.LoginSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def create(self, request):
        serializer = user_serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]
            try:
                check = user_models.User.objects.get(email=email)
                user = authenticate(
                    request, username=request.data["email"], password=request.data["password"])
            except (user_models.User.DoesNotExist, Exception):
                return Response({"status": False, "data": {"message": "Invalid credentials"}}, status=status.HTTP_404_NOT_FOUND)
            if user:
                token = RefreshToken.for_user(user)
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                }
                return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "data": {"message": "Invalid credentials"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": False, "data": {"message": "Invalid credentials", "error": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


class VerifyUserAPIView(APIView):
    permission_classes = [AllowAny]
    lookup_url_kwarg = "verification_token"

    def get(self,  *args, **kwargs):
        verification_token = kwargs.get(self.lookup_url_kwarg)
        try:
            payload = jwt.decode(jwt=verification_token, key=settings.JWT_SECRET, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({"message": "Successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired. Get new one"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CustomerProfileUpdateSerializer

    def get_object(self):
        customer = CustomerProfile.objects.get(user=self.request.user)
        return customer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SubscriptionAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        return super(SubscriptionAPIView, self).post(request, *args, **kwargs)


@api_view(["POST"])
def change_password(request):
    received_json_data = json.loads(request.body)
    user = request.user.id
    try:
        old_password = received_json_data["old_password"]
    except KeyError:
        raise ValidationError("Old password cannot be blank.")
    try:
        new_password = received_json_data["new_password"]
    except KeyError:
        raise ValidationError("New password cannot be blank.")

    try:
        user_obj = User.objects.get(id=user)
    except User.DoesNotExist:
        data = {
            'status': 'failed',
            'code': HTTP_401_UNAUTHORIZED,
            "message": "User is not exists",
            "result": ''
        }
        return Response(data, HTTP_401_UNAUTHORIZED)
    status = check_password(old_password, user_obj.password)

    if not status :
        data = {
            'status': 'failed',
            'code': HTTP_401_UNAUTHORIZED,
            "message": "Your old password is wrong",
            "result": ''
        }
        return Response(data, HTTP_401_UNAUTHORIZED)
    else:
        new_password = make_password(new_password)
        user_obj.password = new_password
        user_obj.save()

        data = {
            'status': 'success',
            'code': HTTP_200_OK,
            "message": "Password changed successfully",
            "result": {
                "user": {
                    "username": user_obj.username,
                    'user_id': user_obj.id
                }
            }
        }
    return Response(data, HTTP_200_OK)