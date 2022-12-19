from django.contrib import admin
from support_ticket.models import Ticket, TicketConversation

class TicketConversationInline(admin.TabularInline):
    model = TicketConversation
    fields = ['conversation_text', 'conversation_photo', 'replier_user']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [
        TicketConversationInline,
    ]
