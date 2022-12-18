from rest_framework import serializers
from support_ticket.models import Ticket

class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'created_at', 'ticket_subject', 'status']

class CustomerTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_subject', 'ticket_description', 'issue_photo']

    def create(self, validated_data):
        ticket_instance = Ticket.objects.create(**validated_data, user=self.context['request'].user)
        return ticket_instance