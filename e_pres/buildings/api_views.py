from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from .models import Building
from .serializers import BuildingSerializer
import json

# Accepts GET and POST
# GET -- return building list
# POST -- saves new building
class RestBuildingListView(ListCreateAPIView):
    serializer_class = BuildingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Building.objects.all()
        return Building.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        #print json.dumps(dict(request.data.iterlists()))
        print request.data
        data = request.data.copy()
        data['user'] = request.user.pk
        print data
        serializer = self.get_serializer(data=data)
        print 'hello'
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
