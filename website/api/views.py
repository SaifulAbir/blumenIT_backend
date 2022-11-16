from rest_framework.generics import RetrieveUpdateAPIView
from website.serializers import *

from website.models import Header


class HeaderAPIView(RetrieveUpdateAPIView):
    serializer_class = HeaderSerializer

    def get_object(self):
        header = Header.objects.get(vendor_admin=self.request.user)
        return header