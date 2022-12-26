from time import time

import pytz
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from datetime import datetime
from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.utils import json
from rest_framework_simplejwt.tokens import RefreshToken

from configs.SMSConfig import OTPManager
from ecommerce.common.emails import send_email_without_delay
from external.validation.data_validator import check_dict_data_rise_error
from user import models as user_models
import jwt
from django.template.loader import render_to_string
from user import serializers as user_serializers
from user.models import CustomerProfile, User, OTPModel
from rest_framework.views import APIView
from user.serializers import  SubscriptionSerializer,  \
    ChangePasswordSerializer, OTPSendSerializer, OTPVerifySerializer, OTPReSendSerializer, SetPasswordSerializer, CustomerOrderListSerializer, \
    CustomerOrderDetailsSerializer, CustomerProfileSerializer, CustomerAddressListSerializer, CustomerAddressSerializer

from vendor.pagination import OrderCustomPagination
from cart.models import Order, DeliveryAddress



class SetPasswordAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = check_dict_data_rise_error("email", request_data=request.data, arrise=True)
        phone = check_dict_data_rise_error("phone", request_data=request.data, arrise=True)
        password = check_dict_data_rise_error("password", request_data=request.data, arrise=True)
        try:
            user = User.objects.get(phone=phone, email=email)
        except User.DoesNotExist:
            user = None
        if user:
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response(
                data={"user_id": user.id if user else None, "details": "Password setup successful"},
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={"user_id": user.id if user else None, "details": "Password setup not successful"},
                status=status.HTTP_400_BAD_REQUEST)


class SendOTPAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OTPSendSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        is_login = check_dict_data_rise_error("is_login", request_data=request.data, arrise=True)
        if is_login == "false":
            email = check_dict_data_rise_error("email", request_data=request.data, arrise=True)
        phone = check_dict_data_rise_error("phone", request_data=request.data, arrise=True)

        if is_login == "false":
            try:
                user_obj = User.objects.get(Q(email=email) | Q(phone=phone))
            except User.DoesNotExist:
                user_obj = None
            if user_obj and user_obj.is_active is True:
            # for user_data in user_obj:
                if user_obj.email == email:
                    return Response({"details": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
                if user_obj.phone == phone:
                    return Response({"details": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

            if not user_obj:
                user = User.objects.create(
                    email=email,
                    phone=phone,
                    username=email,
                    is_customer=True
                )

                user.is_active = False
                user.set_password(phone)
                user.save()
            if user_obj:
                user_obj.set_password(phone)
                user_obj.save()
        # Generate OTP Here
        sent_otp = OTPManager().initialize_otp_and_sms_otp(phone)
        otp_sending_time = datetime.now(pytz.timezone('Asia/Dhaka'))
        otp_model = OTPModel.objects.create(
            contact_number=phone,
            otp_number=sent_otp,
            expired_time=otp_sending_time
        )
        otp_model.save()
        try:
            user = User.objects.get(phone = phone)
            return Response(
                data={"user_id": user.id if user else None, "sent_otp": sent_otp},
                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            user = None
            return Response(
                data={"user_id": user.id if user else None, "sent_otp": sent_otp if user else None},
                status=status.HTTP_404_NOT_FOUND)


class ReSendOTPAPIView(CreateAPIView):
    queryset = OTPModel.objects.all()
    serializer_class = OTPReSendSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        contact_number = check_dict_data_rise_error("contact_number", request_data=request.data, arrise=True)
        sent_otp = OTPManager().initialize_otp_and_sms_otp(contact_number)
        otp_sending_time = datetime.now(pytz.timezone('Asia/Dhaka'))
        try:
            otp_obj = OTPModel.objects.filter(contact_number=contact_number).first()
        except OTPModel.DoesNotExist:
            otp_obj = None
        if not otp_obj:
            return Response({
                'details': "Number doesn't exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        otp_model = OTPModel.objects.create(
            contact_number=contact_number,
            otp_number=sent_otp,
            expired_time=otp_sending_time
        )
        otp_model.save()
        return Response(
            data={"sent_otp": sent_otp},
            status=status.HTTP_201_CREATED)


class OTPVerifyAPIVIEW(CreateAPIView):
    """
       Get OTP from user, and verify it
    """
    serializer_class = OTPVerifySerializer
    queryset = OTPModel.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        contact_number = check_dict_data_rise_error("contact_number", request_data=request.data, arrise=True)
        otp_number = check_dict_data_rise_error("otp_number", request_data=request.data, arrise=True)
        try:
            otp_obj = OTPModel.objects.filter(contact_number=contact_number).last()
            if str(otp_obj.otp_number) == otp_number:
                otp_obj.verified_phone = True
                # OTP matched
                otp_sent_time = otp_obj.expired_time
                timediff = datetime.now(pytz.timezone('Asia/Dhaka')) - otp_sent_time
                time_in_seconds = timediff.total_seconds()

                if time_in_seconds > 120:
                    return Response({
                        'result': 'time expired'
                    }, status=status.HTTP_408_REQUEST_TIMEOUT)
                try:
                    user = User.objects.get(phone=contact_number)
                    user.is_active = True
                    user.save()
                    token = RefreshToken.for_user(user)
                except:
                    pass

                otp_obj.save()
                return Response({"user_id": user.id, "email": user.email, "name": user.name, "phone": user.phone,  'details': 'Verified', "access_token": str(token.access_token) if token else None, "refresh_token": str(token) if token else None}, status=status.HTTP_200_OK)
            else:
                return Response({'details': "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                data={'details': "Number doesn't exists"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


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
                    "name": user.name,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                }
                return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "data": {"message": "Invalid credentials"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": False, "data": {"message": "Invalid credentials", "error": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)

class SuperUserLoginUser(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = user_serializers.SuperAdminLoginSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def create(self, request):
        serializer = user_serializers.SuperAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = authenticate(
                    request, username=request.data["username"], password=request.data["password"])
            except (user_models.User.DoesNotExist, Exception):
                return Response({"status": False, "data": {"message": "Invalid credentials for super user!"}}, status=status.HTTP_404_NOT_FOUND)
            if user:
                user_is_super = user.is_superuser
                if user_is_super == True:
                    token = RefreshToken.for_user(user)
                    data = {
                        "user_id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token)
                    }
                    return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": False, "data": {"message": "Invalid credentials for super user!"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"status": False, "data": {"message": "Invalid credentials for super user!"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": False, "data": {"message": "Invalid credentials for super user!", "error": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


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


class SubscriptionAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        return super(SubscriptionAPIView, self).post(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class CustomerOrdersList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerOrderListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_customer == True:
            queryset = Order.objects.filter(user=self.request.user).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no orders for you."})
        else:
            raise ValidationError(
                {"msg": 'You can not show order list, because you are not an User!'})


class CustomerOrderDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerOrderDetailsSerializer
    lookup_field = 'o_id'
    lookup_url_kwarg = "o_id"

    def get_object(self):
        o_id = self.kwargs['o_id']
        if self.request.user.is_customer == True:
            query = Order.objects.get(id=o_id, user=self.request.user)
            if query:
                return query
            else:
                raise ValidationError({"msg": "This is not your order or Order not available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not show order details, because you are not an User!'})


class CustomerProfile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user_id = self.kwargs['id']
        if self.request.user.is_customer == True:
            query = User.objects.filter(id=user_id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'User data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update show or update profile, because you are not an Customer!'})


class CustomerAddressListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerAddressListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_customer == True:
            queryset = DeliveryAddress.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no orders for you."})
        else:
            raise ValidationError(
                {"msg": 'You can not show address list, because you are not an Customer!'})


class CustomerAddressAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerAddressSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_customer == True:
            return super(CustomerAddressAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not add address, because you are not an Customer!'})


class CustomerAddressUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerAddressSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        addr_id = self.kwargs['id']
        if self.request.user.is_customer == True:
            query = DeliveryAddress.objects.filter(id=addr_id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Address data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update show or update address, because you are not an Customer!'})


class CustomerAddressDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerAddressListSerializer
    pagination_class = OrderCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_customer == True:
            address_obj_exist = DeliveryAddress.objects.filter(id=id).exists()
            if address_obj_exist:
                address_obj = DeliveryAddress.objects.filter(id=id)
                address_obj.update(is_active=False)

                queryset = DeliveryAddress.objects.filter(user=self.request.user, is_active = True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Address Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this address, because you are not an Customer!'})


class DashboardDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.user.is_customer == True:
            customer_profile = User.objects.filter(id=self.request.user.id)
            customer_profile_serializer = CustomerProfileSerializer(customer_profile, many=True, context={"request": request})

            all_orders_count = Order.objects.filter(user=self.request.user.id).count()
            awaiting_payments_count = Order.objects.filter(Q(user=self.request.user.id), Q(payment_status='UN-PAID')).count()
            awaiting_shipment_count = Order.objects.filter(Q(user=self.request.user.id), Q(order_status='PENDING') | Q(order_status='CONFIRMED')).count()
            awaiting_delivery_count = Order.objects.filter(Q(user=self.request.user.id), Q(order_status='PICKED-UP')).count()

            return Response({
                "customer_profile": customer_profile_serializer.data,
                "all_orders_count": all_orders_count,
                "awaiting_payments_count": awaiting_payments_count,
                'awaiting_shipment_count':awaiting_shipment_count,
                "awaiting_delivery_count": awaiting_delivery_count
            })

        else:
            raise ValidationError(
                {"msg": 'You can not get dashboard data, because you are not an Customer!'})




# class CustomerRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     serializer_class = CustomerProfileUpdateSerializer
#
#     def get_object(self):
#         customer = CustomerProfile.objects.get(user=self.request.user)
#         return customer
#
#     # def put(self, request, *args, **kwargs):
#     #     return self.update(request, *args, **kwargs)

# @api_view(["POST"])
# def change_password(request):
#     received_json_data = json.loads(request.body)
#     user = request.user.id
#     try:
#         old_password = received_json_data["old_password"]
#     except KeyError:
#         raise ValidationError("Old password cannot be blank.")
#     try:
#         new_password = received_json_data["new_password"]
#     except KeyError:
#         raise ValidationError("New password cannot be blank.")
#
#     try:
#         user_obj = User.objects.get(id=user)
#     except User.DoesNotExist:
#         data = {
#             'status': 'failed',
#             'code': HTTP_401_UNAUTHORIZED,
#             "message": "User is not exists",
#             "result": ''
#         }
#         return Response(data, HTTP_401_UNAUTHORIZED)
#     status = check_password(old_password, user_obj.password)
#
#     if not status :
#         data = {
#             'status': 'failed',
#             'code': HTTP_401_UNAUTHORIZED,
#             "message": "Your old password is wrong",
#             "result": ''
#         }
#         return Response(data, HTTP_401_UNAUTHORIZED)
#     else:
#         new_password = make_password(new_password)
#         user_obj.password = new_password
#         user_obj.save()
#
#         data = {
#             'status': 'success',
#             'code': HTTP_200_OK,
#             "message": "Password changed successfully",
#             "result": {
#                 "user": {
#                     "username": user_obj.username,
#                     'user_id': user_obj.id
#                 }
#             }
#         }
#     return Response(data, HTTP_200_OK)


# class UserListAPIView(ListAPIView):
#     queryset = User.objects.filter()
#     permission_classes = [AllowAny]
#     serializer_class = UserRegisterSerializer


# class RegisterUser(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = user_models.User.objects.all()
#     serializer_class = user_serializers.UserRegisterSerializer
#     permission_classes = [AllowAny]
#
#     def create(self, request):
#         serializer = user_serializers.UserRegisterSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             user = user_models.User.objects.none()
#             try:
#                 user = user_models.User.objects.get(
#                     email=request.data["email"])
#
#                 token = RefreshToken.for_user(user)
#
#                 exp = time() + 1200 #20 minutes
#                 email_list = request.data["email"]
#                 subject = "Verify Your Account"
#                 token = jwt.encode({'email': email_list, 'exp': exp, 'scope': subject},
#                                    settings.JWT_SECRET, algorithm='HS256')
#                 html_message = render_to_string('verification_email.html', {'token': token, 'domain': settings.EMAIL_DOMAIN_NAME})
#                 send_email_without_delay(subject, html_message, email_list)
#                 CustomerProfile.objects.create(user=user)
#                 data = {
#                     "user_id": user.id,
#                     "email": user.email,
#                     "full_name": user.first_name + " " + user.last_name
#                 }
#                 return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
#             except (user_models.User.DoesNotExist):
#                 if user:
#                     user.delete()
#                 return Response({"status": False, "data": {"message": "User not registered. Please try again."}}, status=status.HTTP_409_CONFLICT)
#         else:
#             return Response({"status": False, "data": {"message": "User not registered. Please try again.", "errors": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)