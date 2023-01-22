from rest_framework import serializers
from support_ticket.models import Ticket, TicketConversation

class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'created_at', 'ticket_subject', 'status']


class TicketConversationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    user_name = serializers.CharField(source='ticket.user.email',read_only=True)
    class Meta:
        model = TicketConversation
        fields = ['id', 'conversation_text', 'conversation_photo', 'created_at', 'user_name' ]


class CustomerTicketCreateSerializer(serializers.ModelSerializer):
    ticket_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    ticket_conversation = TicketConversationSerializer(many=True, required=False)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'ticket_subject', 'ticket_conversation', 'created_at', 'status']

    def create(self, validated_data):
        # ticket_conversation
        try:
            ticket_conversations = validated_data.pop('ticket_conversation')
        except:
            ticket_conversations = ''

        ticket_instance = Ticket.objects.create(**validated_data, user=self.context['request'].user)

        # ticket_conversation
        if ticket_conversations:
            for ticket_conversation in ticket_conversations:
                conversation_text = ticket_conversation['conversation_text']
                try:
                    conversation_photo = ticket_conversation['conversation_photo']
                except:
                    conversation_photo = ''

                if conversation_text:
                    ticket_conversation_instance = TicketConversation.objects.create(conversation_text=conversation_text,  conversation_photo=conversation_photo, ticket=ticket_instance, replier_user=self.context['request'].user)

        return ticket_instance


class TicketDataSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username',read_only=True)
    ticket_conversation = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'user_name', 'created_at', 'status', 'ticket_subject', 'ticket_conversation']

    def get_ticket_conversation(self, obj):
        selected_ticket_conversation = TicketConversation.objects.filter(
            ticket=obj, is_active=True).order_by('id')
        return TicketConversationSerializer(selected_ticket_conversation, many=True).data


class TicketConversationReplySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    user_name = serializers.CharField(source='ticket.user.username',read_only=True)
    class Meta:
        model = TicketConversation
        fields = ['id', 'ticket', 'conversation_text', 'conversation_photo', 'created_at', 'user_name' ]

    def create(self, validated_data):
        ticket_conversation_instance = TicketConversation.objects.create(**validated_data, replier_user=self.context['request'].user)
        return ticket_conversation_instance