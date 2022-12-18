from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from support_ticket.api.views import CustomerTicketListAPI, CustomerTicketCreateAPIView

urlpatterns = [
    path('customer-ticket-list/', CustomerTicketListAPI.as_view()),
    path('customer-ticket-create/', CustomerTicketCreateAPIView.as_view()),
]