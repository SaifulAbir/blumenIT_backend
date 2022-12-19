from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from support_ticket.api.views import CustomerTicketListAPI, CustomerTicketCreateAPIView, CustomerTicketDetailsAPIView, \
    CustomerTicketReplyAPIView

urlpatterns = [
    path('support-ticket/customer-ticket-list/', CustomerTicketListAPI.as_view()),
    path('support-ticket/customer-ticket-create/', CustomerTicketCreateAPIView.as_view()),
    path('support-ticket/customer-ticket-details/<int:id>/', CustomerTicketDetailsAPIView.as_view()),
    path('support-ticket/customer-ticket-reply/', CustomerTicketReplyAPIView.as_view()),
]