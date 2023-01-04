from rest_framework.generics import ListAPIView, CreateAPIView
from support_ticket.models import Ticket
from rest_framework.permissions import IsAuthenticated
from vendor.pagination import OrderCustomPagination
from support_ticket.serializers import TicketListSerializer, CustomerTicketCreateSerializer, TicketDataSerializer, \
    TicketConversationReplySerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q

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
    serializer_class = CustomerTicketCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_customer == True:
            return super(CustomerTicketCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create ticket, because you are not an User!'})


class CustomerTicketDetailsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketDataSerializer
    def get_queryset(self):
        ticket_id = self.kwargs['id']
        if self.request.user.is_customer == True:
            if ticket_id:
                queryset = Ticket.objects.filter(Q(id=ticket_id)).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": 'Ticket details not found!'})
        else:
            raise ValidationError({"msg": 'You can not see ticket details, because you are not an Customer!'})


class CustomerTicketReplyAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketConversationReplySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_customer == True:
            return super(CustomerTicketReplyAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create ticket reply, because you are not an User!'})