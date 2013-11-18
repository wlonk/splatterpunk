from rest_framework import generics

from .models import Sheet
from .serializers import SheetSerializer


class SheetListView(generics.ListAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer


class SheetInstanceView(generics.RetrieveAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
