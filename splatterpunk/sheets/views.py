from rest_framework import (
    generics,
    permissions,
)

from .models import Sheet
from .serializers import SheetSerializer


class SheetListView(generics.ListCreateAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def pre_save(self, obj):
        obj.user = self.request.user


class SheetInstanceView(generics.RetrieveAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
