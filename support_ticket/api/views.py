from rest_framework.generics import ListAPIView, CreateAPIView
from support_ticket.models import Ticket
from rest_framework.permissions import AllowAny, IsAuthenticated
from vendor.pagination import OrderCustomPagination
from support_ticket.serializers import TicketListSerializer, TicketSerializer
from rest_framework.exceptions import ValidationError

class CustomerTicketListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_customer == True:
            queryset = Ticket.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no ticket in your ticket list."})
        else:
            raise ValidationError(
                {"msg": 'You can not show ticket list, because you are not an User!'})


class CustomerTicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_customer == True:
            return super(CustomerTicketCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not show ticket list, because you are not an User!'})