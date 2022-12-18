from rest_framework import serializers
from support_ticket.models import Ticket, TicketConversation

class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'created_at', 'ticket_subject', 'status']


class TicketConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketConversation
        fields = ['id', 'conversation_text', 'conversation_photo']

class CustomerTicketCreateSerializer(serializers.ModelSerializer):
    ticket_id = serializers.CharField(read_only=True)
    ticket_conversation = TicketConversationSerializer(many=True, required=False)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'ticket_subject', 'ticket_conversation']

    def create(self, validated_data):
        ticket_instance = Ticket.objects.create(**validated_data, user=self.context['request'].user)
        return ticket_instance