from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Sheet
from .serializers import SheetSerializer
from .permissions import IsOwnerOrReadOnly


class SheetListView(generics.ListCreateAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def pre_save(self, obj):
        obj.user = self.request.user


class SheetInstanceView(generics.RetrieveUpdateAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
