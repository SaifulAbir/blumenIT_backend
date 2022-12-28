from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from user.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from stuff.serializers import StuffListSerializer, CreateStuffSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from external.validation.data_validator import check_dict_data_rise_error
from rest_framework import status
from django.db.models import Q
from stuff.models import Role


class StuffListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StuffListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = User.objects.filter(is_staff=True, is_active=True)

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no stuff data in stuff list."})
        else:
            raise ValidationError(
                {"msg": 'You can not show stuff list, because you are not an Admin!'})


class CreateStuffAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateStuffSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            name = check_dict_data_rise_error("name", request_data=request.data, arrise=True)
            email = check_dict_data_rise_error("email", request_data=request.data, arrise=True)
            phone = check_dict_data_rise_error("phone", request_data=request.data, arrise=True)
            password = check_dict_data_rise_error("password", request_data=request.data, arrise=True)
            role = check_dict_data_rise_error("role", request_data=request.data, arrise=True)

            try:
                user_obj = User.objects.get(Q(email=email) | Q(phone=phone))
            except User.DoesNotExist:
                user_obj = None

            if not user_obj:
                # create stuff user 
                user = User.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    role=Role.objects.get(id=role),
                    username=email,
                    is_staff=True
                )

                user.is_active = True
                user.set_password(password)
                user.save()

                return Response(
                data={"user_id": user.id if user else None},
                status=status.HTTP_201_CREATED)
            else:
                if user_obj.email == email:
                    return Response({"details": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
                if user_obj.phone == phone:
                    return Response({"details": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)


            return Response({"details": role}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError(
                {"msg": 'You can not create stuff, because you are not an Admin!'})