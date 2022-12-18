from django.db import models
from ecommerce.models import AbstractTimeStamp
from user.models import User
from .utils import unique_slug_generator_support

class Ticket(AbstractTimeStamp):
    TICKET_STATUSES = [
        ('NOT-RESOLVED', 'Not-Resolved'),
        ('RESOLVED', 'Resolved'),
    ]

    ticket_id = models.SlugField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='ticket_creator_user', blank=True, null=True)
    ticket_subject = models.CharField(max_length=255, null=False, blank=False)
    ticket_description = models.TextField(null=True, blank=True)
    issue_photo = models.FileField(upload_to='ticket_photo', blank=True, null=True)
    solution_photo = models.FileField(upload_to='ticket_photo', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=TICKET_STATUSES, default=TICKET_STATUSES[0][0])

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'tickets'
        db_table = 'ticket'

    def __str__(self):
        return self.ticket_id

def pre_save_support(sender, instance, *args, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = '#' + \
            str(unique_slug_generator_support(instance))

class TicketConversation(AbstractTimeStamp):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_conversation_ticket', blank=True, null=True)
    conversation_text = models.TextField(null=False, blank=False)
    replier_user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='replier_user', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'TicketConversation'
        verbose_name_plural = 'ticket_conversations'
        db_table = 'ticket_conversation'

    def __str__(self):
        return self.ticket.ticket_id