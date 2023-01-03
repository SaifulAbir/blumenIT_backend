from django.db import models
from ecommerce.models import AbstractTimeStamp

class File(AbstractTimeStamp):
    file = models.FileField(blank=False, null=False)
    name = models.CharField(max_length=254, null=True, editable=False)
    size = models.PositiveBigIntegerField(null=True, editable=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
