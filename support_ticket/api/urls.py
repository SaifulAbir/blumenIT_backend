from django.urls import path
from support_ticket.api.views import CustomerTicketListAPI, CustomerTicketCreateAPIView, CustomerTicketDetailsAPIView, \
    CustomerTicketReplyAPIView

urlpatterns = [
    path('support-ticket/customer-ticket-list/', CustomerTicketListAPI.as_view(), name='ticket_list'),
    path('support-ticket/customer-ticket-create/', CustomerTicketCreateAPIView.as_view(), name='ticket_create'),
    path('support-ticket/customer-ticket-details/<int:id>/', CustomerTicketDetailsAPIView.as_view(), name='ticket_details'),
    path('support-ticket/customer-ticket-reply/', CustomerTicketReplyAPIView.as_view(), name='ticket_reply'),
]