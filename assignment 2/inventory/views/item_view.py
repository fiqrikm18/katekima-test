from rest_framework import status as http_status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Item
from ..serializers.item_serializer import ItemSerializer


class ItemView(ModelViewSet):
    # renderer_classes = [api_response.CustomJsonRenderer]
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('-id')

    def retrieve(self, request, *args, **kwargs):
        item = (Item
                .objects
                .filter(code=kwargs.get('code'))
                .values('code', 'name', 'unit', 'description', 'stock', 'balance'))

        if not item:
            raise NotFound

        return Response(item, status=http_status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            item = Item.objects.filter(code=kwargs.get('code')).get()
            serializer = self.get_serializer(request.data)

            if serializer.data['name'] is not None or serializer.data['name'] != '' or serializer.data[
                'name'] != item.name:
                item.name = serializer.data['name']

            if serializer.data['description'] is not None or serializer.data['description'] != '' or serializer.data[
                'description'] != item.description:
                item.description = serializer.data['description']

            if serializer.data['unit'] is not None or serializer.data['unit'] != '' or serializer.data[
                'unit'] != item.unit:
                item.unit = serializer.data['unit']

            if serializer.data['balance'] is not None or serializer.data['balance'] != '' or serializer.data[
                'balance'] != item.balance:
                item.balance = serializer.data['balance']

            if serializer.data['stock'] is not None or serializer.data['stock'] != '' or serializer.data[
                'stock'] != item.stock:
                item.stock = serializer.data['stock']

            item.save()
            return Response([], status=http_status.HTTP_200_OK)
        except Item.DoesNotExist:
            raise NotFound

    def destroy(self, request, *args, **kwargs):
        try:
            item = Item.objects.filter(code=kwargs.get('code')).get()
            item.soft_deleted()

            return Response([], status=http_status.HTTP_200_OK)
        except Item.DoesNotExist:
            raise NotFound
