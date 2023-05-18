from time import time

import pytz
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db.models import Q
from datetime import datetime
from rest_framework import viewsets, mixins, status, generics, response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
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
from user.serializers import SubscriptionSerializer, \
    ChangePasswordSerializer, OTPSendSerializer, OTPVerifySerializer, OTPReSendSerializer, SetPasswordSerializer, \
    CustomerOrderListSerializer, \
    CustomerOrderDetailsSerializer, CustomerProfileSerializer, CustomerAddressListSerializer, CustomerAddressSerializer, \
    WishlistDataSerializer, SavePcCreateSerializer, SavaPcDataSerializer, SavePcDetailsSerializer, \
    AccountDeleteRequestSerializer, AccountDeleteSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, SignUpSerializer

from vendor.pagination import OrderCustomPagination
from cart.models import Order, DeliveryAddress, Wishlist
from product.models import SavePc, SavePcItems

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.core.mail import send_mail
from django.http import QueryDict


class SetPasswordAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = check_dict_data_rise_error(
            "email", request_data=request.data, arrise=True)
        phone = check_dict_data_rise_error(
            "phone", request_data=request.data, arrise=True)
        password = check_dict_data_rise_error(
            "password", request_data=request.data, arrise=True)
        try:
            user = User.objects.get(phone=phone, email=email)
        except User.DoesNotExist:
            user = None
        if user:
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response(
                data={"user_id": user.id if user else None,
                      "details": "Password setup successful"},
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={"user_id": user.id if user else None,
                      "details": "Password setup not successful"},
                status=status.HTTP_400_BAD_REQUEST)


class SendOTPAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OTPSendSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        is_login = check_dict_data_rise_error(
            "is_login", request_data=request.data, arrise=True)
        if is_login == "false":
            email = check_dict_data_rise_error(
                "email", request_data=request.data, arrise=True)
        phone = check_dict_data_rise_error(
            "phone", request_data=request.data, arrise=True)
        name = check_dict_data_rise_error(
            "full_name", request_data=request.data, arrise=False)

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
                    name=name,
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
            user = User.objects.get(phone=phone)
            return Response(
                data={"user_id": user.id if user else None, "sent_otp": sent_otp},
                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            user = None
            return Response(
                data={"user_id": user.id if user else None,
                      "sent_otp": sent_otp if user else None},
                status=status.HTTP_404_NOT_FOUND)


class ReSendOTPAPIView(CreateAPIView):
    queryset = OTPModel.objects.all()
    serializer_class = OTPReSendSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        contact_number = check_dict_data_rise_error(
            "contact_number", request_data=request.data, arrise=True)
        sent_otp = OTPManager().initialize_otp_and_sms_otp(contact_number)
        otp_sending_time = datetime.now(pytz.timezone('Asia/Dhaka'))
        try:
            otp_obj = OTPModel.objects.filter(
                contact_number=contact_number).first()
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
        contact_number = check_dict_data_rise_error(
            "contact_number", request_data=request.data, arrise=True)
        otp_number = check_dict_data_rise_error(
            "otp_number", request_data=request.data, arrise=True)
        try:
            otp_obj = OTPModel.objects.filter(
                contact_number=contact_number).last()
            if str(otp_obj.otp_number) == otp_number:
                otp_obj.verified_phone = True
                # OTP matched
                otp_sent_time = otp_obj.expired_time
                timediff = datetime.now(
                    pytz.timezone('Asia/Dhaka')) - otp_sent_time
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


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        is_login = check_dict_data_rise_error(
            "is_login", request_data=request.data, arrise=True)
        if is_login == "false":
            email = check_dict_data_rise_error(
                "email", request_data=request.data, arrise=True)
        phone = check_dict_data_rise_error(
            "phone", request_data=request.data, arrise=True)
        password = check_dict_data_rise_error(
            "password", request_data=request.data, arrise=True)

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

                user.is_active = True
                user.set_password(password)
                user.save()
            if user_obj:
                user_obj.set_password(password)
                user_obj.save()
        try:
            user = User.objects.get(phone=phone)
            return Response(
                data={"user_id": user.id if user else None},
                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            user = None
            return Response(
                data={"user_id": user.id if user else None},
                status=status.HTTP_404_NOT_FOUND)


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
                user_name = User.objects.get(
                    email=request.data["email"]).username
                user = authenticate(
                    request, username=user_name, password=request.data["password"])
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
        serializer = user_serializers.SuperAdminLoginSerializer(
            data=request.data)
        if serializer.is_valid():
            try:
                user = authenticate(
                    request, username=request.data["username"], password=request.data["password"])
            except (user_models.User.DoesNotExist, Exception):
                return Response({"status": False, "data": {"message": "Invalid credentials for super user!"}}, status=status.HTTP_404_NOT_FOUND)

            if user:
                user_is_super = user.is_superuser
                user_is_staff = user.is_staff
                user_is_seller = user.is_seller
                if user_is_super == True:
                    token = RefreshToken.for_user(user)
                    data = {
                        "user_id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                        "user_is_super": True,
                        "is_staff": False,
                        "is_seller": False,
                    }
                    return Response({"status": True, "data": data}, status=status.HTTP_200_OK)

                elif user_is_staff == True:
                    token = RefreshToken.for_user(user)
                    data = {
                        "user_id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                        "user_is_super": False,
                        "is_staff": True,
                        "is_seller": False,
                    }
                    return Response({"status": True, "data": data}, status=status.HTTP_200_OK)

                elif user_is_seller == True:
                    token = RefreshToken.for_user(user)
                    data = {
                        "user_id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                        "user_is_super": False,
                        "is_staff": False,
                        "is_seller": True,
                    }
                    return Response({"status": True, "data": data}, status=status.HTTP_200_OK)

                else:
                    return Response({"status": False, "data": {"message": "Invalid credentials!"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"status": False, "data": {"message": "Invalid credentials!"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": False, "data": {"message": "Invalid credentials!", "error": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


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
            queryset = Order.objects.filter(
                user=self.request.user).order_by('-created_at')

            if queryset:
                return queryset
            else:
                return []
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
                raise ValidationError(
                    {"msg": "This is not your order or Order not available! "})
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
            raise ValidationError(
                {"msg": 'You can not update show or update profile, because you are not an Customer!'})


class CustomerAddressListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerAddressListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_customer == True:
            queryset = DeliveryAddress.objects.filter(
                user=self.request.user, is_active=True).order_by('-created_at')

            if queryset:
                return queryset
            else:
                return []
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
            raise ValidationError(
                {"msg": 'You can not update show or update address, because you are not an Customer!'})


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

                queryset = DeliveryAddress.objects.filter(
                    user=self.request.user, is_active=True).order_by('-created_at')
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
            customer_profile_serializer = CustomerProfileSerializer(
                customer_profile, many=True, context={"request": request})

            all_orders_count = Order.objects.filter(
                user=self.request.user.id).count()
            awaiting_payments_count = Order.objects.filter(
                Q(user=self.request.user.id), Q(payment_status='UN-PAID')).count()
            awaiting_shipment_count = Order.objects.filter(Q(user=self.request.user.id), Q(
                order_status='PENDING') | Q(order_status='CONFIRMED')).count()
            awaiting_delivery_count = Order.objects.filter(
                Q(user=self.request.user.id), Q(order_status='PICKED-UP')).count()

            return Response({
                "customer_profile": customer_profile_serializer.data,
                "all_orders_count": all_orders_count,
                "awaiting_payments_count": awaiting_payments_count,
                'awaiting_shipment_count': awaiting_shipment_count,
                "awaiting_delivery_count": awaiting_delivery_count
            })

        else:
            raise ValidationError(
                {"msg": 'You can not get dashboard data, because you are not an Customer!'})


class WishlistDataAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistDataSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        # def get(self, request):
        if self.request.user.is_customer == True:
            wishlist_obj_exist = Wishlist.objects.filter(
                Q(user=self.request.user)).exists()
            if wishlist_obj_exist:
                queryset = Wishlist.objects.filter(
                    Q(user=self.request.user)).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Wishlist data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not see Wishlist data, because you are not an Customer!'})


class SavePcAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavePcCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_customer == True:
            uid = User.objects.get(id=self.request.user.id)
            if uid:
                return super(SavePcAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError({"msg": 'You are not a Customer.'})


class SavePcListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavaPcDataSerializer

    def get_queryset(self):
        if self.request.user.is_customer == True:
            save_pc_obj_exist = SavePc.objects.filter(
                Q(user=self.request.user), Q(is_active=True)).exists()
            if save_pc_obj_exist:
                queryset = SavePc.objects.filter(Q(user=self.request.user), Q(
                    is_active=True)).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Save Pc data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not see Save Pc data, because you are not an Customer!'})


class SavePcViewAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavePcDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        id = self.kwargs['id']
        if self.request.user.is_customer == True:
            save_pc_obj_exist = SavePc.objects.filter(id=id).exists()
            if save_pc_obj_exist:
                query = SavePc.objects.get(id=id)
                return query
            else:
                raise ValidationError(
                    {"msg": 'Save Pc Items data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not see Save Pc data, because you are not an Customer!'})


class SavePcDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavaPcDataSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_customer == True:
            save_pc_obj_exist = SavePc.objects.filter(id=id).exists()
            if save_pc_obj_exist:
                save_pc_obj = SavePc.objects.filter(id=id)
                save_pc_obj.update(is_active=False)

                queryset = SavePc.objects.filter(Q(user=self.request.user), Q(
                    is_active=True)).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Save Pc data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this Save PC data, because you are not an Customer!'})


class AccountDeleteRequestAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDeleteRequestSerializer
    queryset = User.objects.all()


class AdminAccountDeleteRequestListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDeleteRequestSerializer
    pagination_class = OrderCustomPagination
    queryset = User.objects.filter(delete_request=True)


class AdminAccountDeleteAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDeleteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        user = User.objects.filter(id=id)
        return user

    def put(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        request = self.request

        active = request.GET.get('is_active')

        email = user.email
        subject = "Confirmation of account deletion"
        html_message = render_to_string('confirmation_of_account_delete.html', {
                                        'active': active, 'user': user})

        send_mail(
            subject=subject,
            message=None,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message
        )

        return self.update(request, *args, **kwargs)


class ForgotPasswordCustomerView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            encoded_uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # reset_url = request.build_absolute_uri(reverse('reset-password'))
            reset_url = f"https://blumanit.vercel.app/reset-password/?encoded_uid={encoded_uid}&token={token}"

            subject = "Reset Your Password"
            message = f"Click the following link to reset your password: {reset_url}"

            recipient_list = [email]
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            # send email
            # email_message.send()
            return response.Response(
                {
                    "message": "Password reset email sent",
                    # "message":
                    #     f"Your Password reset link: {reset_url}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            encoded_uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # reset_url = request.build_absolute_uri(reverse('reset-password'))
            reset_url = f"https://blumen-it-admin.vercel.app/reset-password/?encoded_uid={encoded_uid}&token={token}"

            subject = "Reset Your Password"
            message = f"Click the following link to reset your password: {reset_url}"

            recipient_list = [email]
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            # send email
            # email_message.send()
            return response.Response(
                {
                    "message": "Password reset email sent",
                    # "message":
                    #     f"Your Password reset link: {reset_url}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        # query_params = QueryDict(request.META['QUERY_STRING'])
        # encoded_uid = query_params.get('encoded_uid')
        # token = query_params.get('token')
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )

        #     email = serializer.validated_data['email']
        #     user = User.objects.filter(email=email).first()
        #     if user:
        #         user_id = urlsafe_base64_encode(force_bytes(user.id))
        #         token = default_token_generator.make_token(user)
        #         reset_url = f'{settings.FRONTEND_URL}/reset-password/{user_id}/{token}/'
        #
        #         send_mail(
        #             'Password reset request',
        #             f'Click on the link to reset your password: {reset_url}',
        #             settings.DEFAULT_FROM_EMAIL,
        #             [email],
        #             fail_silently=False
        #         )
        #     return Response({'success': 'Password reset email has been sent'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
