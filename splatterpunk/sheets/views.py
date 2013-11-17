from rest_framework import generics

from .models import Sheet


class SheetView(generics.ListAPIView):
    model = Sheet
