from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from user.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from stuff.serializers import StuffListSerializer, CreateStuffSerializer, UpdateStuffSerializer, RoleListSerializer, RoleCreateSerializer, \
    RoleUpdateSerializer, PermissionSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from external.validation.data_validator import check_dict_data_rise_error
from rest_framework import status
from django.db.models import Q
from stuff.models import Role, PermissionModules


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


class UpdateStuffAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateStuffSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        stuff_id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = User.objects.filter(Q(id=stuff_id), Q(is_staff=True))
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Stuff does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update Stuff info, because you are not an Admin!'})


    def put(self, request, *args, **kwargs):
        try:
            try:
                name = request.data["name"]
            except:
                name = None
            try:
                email = request.data["email"]
            except:
                email = None
            try:
                phone = request.data["phone"]
            except:
                phone = None
            try:
                password = request.data["password"]
            except:
                password = None
            try:
                role = request.data["role"]
            except:
                role = None

            stuff_id = self.kwargs['id']

            try:
                stuff_obj = User.objects.get(id=stuff_id)
            except:
                stuff_obj = None

            if stuff_obj:
                if name:
                    stuff_obj.name = name

                if email:
                    current_user_email = stuff_obj.email
                    if User.objects.filter(email__iexact=email).exclude(email__iexact=current_user_email).count() > 0:
                        raise ValidationError({"msg": 'This email address is already in use.'})
                    else:
                        stuff_obj.email = email
                        stuff_obj.username = email

                if phone:
                    current_user_phone = stuff_obj.phone
                    if User.objects.filter(phone__iexact=phone).exclude(phone__iexact=current_user_phone).count() > 0:
                        raise ValidationError({"msg": 'This phone is already in use.'})
                    else:
                        stuff_obj.phone = phone

                if password:
                    stuff_obj.set_password(password)

                if role:
                    try:
                        stuff_obj.role = Role.objects.get(id=role)
                    except:
                        raise ValidationError({"msg": 'You provided a wrong role id'})

                stuff_obj.save()
                return Response(data={"user_id": stuff_obj.id}, status=status.HTTP_202_ACCEPTED)
            else:
                raise ValidationError({"msg": 'Stuff update failed!'})
        except KeyError:
            raise ValidationError({"msg": 'Stuff update failed. contact with developer!'})


class RoleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoleListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Role.objects.all()

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no role data in role list."})
        else:
            raise ValidationError(
                {"msg": 'You can not show role list, because you are not an Admin!'})


class AdminRoleCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoleCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminRoleCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create product, because you are not an Admin!'})


class AdminRoleUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoleUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = Role.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Role does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update role, because you are not an Admin!'})


class PermissionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = PermissionModules.objects.all()

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no permission modules data in permission modules list."})
        else:
            raise ValidationError(
                {"msg": 'You can not show permission modules list, because you are not an Admin!'})


class AdminPermissionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminPermissionCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create permission, because you are not an Admin!'})


class AdminPermissionUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = PermissionModules.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Permission Modules does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update permission modules, because you are not an Admin!'})