from djangoldp.views import LDPViewSet
from rest_framework.response import Response
from rest_framework import status


class InvoiceLDPViewSet(LDPViewSet):
    def list(self, request, *args, **kwargs):
        '''overridden so that it can only be accessed from a nested field, not globally'''
        if not hasattr(self, 'nested_field'):
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
