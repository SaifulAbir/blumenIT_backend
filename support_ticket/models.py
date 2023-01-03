from django.db import models
from ecommerce.models import AbstractTimeStamp
from user.models import User
from .utils import unique_slug_generator_ticket
from django.db.models.signals import pre_save

class Ticket(AbstractTimeStamp):
    TICKET_STATUSES = [
        ('NOT-RESOLVED', 'Not-Resolved'),
        ('RESOLVED', 'Resolved'),
    ]

    ticket_id = models.SlugField(null=False, allow_unicode=True, blank=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='ticket_creator_user', blank=True, null=True)
    ticket_subject = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=TICKET_STATUSES, default=TICKET_STATUSES[0][0])

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'tickets'
        db_table = 'ticket'

    def __str__(self):
        return self.ticket_subject + ' ticket_id: '+ self.ticket_id

def pre_save_ticket(sender, instance, *args, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = unique_slug_generator_ticket(instance)
pre_save.connect(pre_save_ticket, sender=Ticket)

class TicketConversation(AbstractTimeStamp):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_conversation_ticket', blank=True, null=True)
    conversation_text = models.TextField(null=False, blank=False)
    conversation_photo = models.FileField(upload_to='ticket_photo', blank=True, null=True)
    replier_user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='replier_user', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'TicketConversation'
        verbose_name_plural = 'ticket_conversations'
        db_table = 'ticket_conversation'

    def __str__(self):
        return self.ticket.ticket_id