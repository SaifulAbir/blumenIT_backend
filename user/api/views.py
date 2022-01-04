from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from user import models as user_models
from user import serializers as user_serializers


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
                data = {
                    "email": user.email,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
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