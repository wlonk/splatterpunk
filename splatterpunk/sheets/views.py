from rest_framework import (
    generics,
    status,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .constants import SHEET_TEMPLATES
from .models import Sheet
from .serializers import SheetSerializer
from .permissions import IsOwnerOrReadOnly


class SheetListView(generics.ListCreateAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def create(self, request, *args, **kwargs):
        # Note that we don't get a pre-save here, because this is a comple
        # object that can't be made in memory independent of the database.
        try:
            name = request.POST['name']
            template = request.POST.get('template', 'mortal')
            if template not in SHEET_TEMPLATES.keys():
                raise ValueError
            self.object = Sheet.objects.with_template(
                template,
                request.user,
                name
            )
        except KeyError:
            return Response(
                {'error': 'You must specify a name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response(
                {
                    'error': '{template} is not a valid template'.format(
                        template=template
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            self.post_save(self.object, created=True)
            serializer = self.get_serializer(self.object)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )


class SheetInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
