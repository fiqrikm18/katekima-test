from django.shortcuts import get_object_or_404
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from inventory.models import Item
from ..models import Transaction, TransactionDetail
from ..serializers import transaction_serialize


class SellView(viewsets.ModelViewSet):
    queryset = Transaction.objects.filter(transaction_type='sell')
    serializer_class = transaction_serialize.TransactionSerialize

    def list(self, request, *args, **kwargs):
        sell_transactions = (Transaction
                             .objects
                             .filter(transaction_type='sell')
                             .all())

        return Response(sell_transactions, status=http_status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        fields = [f.name for f in Transaction._meta.get_fields()]
        fields.remove('transaction_type')

        sell_transactions = (Transaction
                             .objects
                             .filter(transaction_type='sell', code=kwargs.get('code'))
                             .values(*fields).get())

        sell_serialize = self.get_serializer(sell_transactions)
        return Response(sell_serialize.data, status=http_status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['transaction_type'] = 'sell'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response([], status=http_status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            serialize_request = self.get_serializer(request.data)
            sell = Transaction.objects.filter(code=kwargs.get('code')).get()

            if (serialize_request.data['description'] is not None or
                    serialize_request.data['description'] != sell.description):
                sell.description = serialize_request.data['description']

            if serialize_request.data['date'] is not None or serialize_request.data['date'] != sell.date:
                sell.date = serialize_request.data['date']

            sell.save()
            sell_serialize = self.get_serializer(sell)
            return Response(sell_serialize.data, status=http_status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            raise NotFound

    def destroy(self, request, *args, **kwargs):
        try:
            sell = Transaction.objects.filter(code=kwargs.get('code')).get()
            sell.soft_deleted()
        except Transaction.DoesNotExist:
            raise NotFound

    @action(methods=['post'], detail=False, name='create detail sell')
    def crate_detail_sell(self, request, *args, **kwargs):
        try:
            get_object_or_404(Transaction, code=kwargs.get('code'))  # check if transaction exist
            item = get_object_or_404(Item, code=request.data['item_code'])  # check if item exist

            request.data['header_code'] = kwargs.get('code')
            serializer = transaction_serialize.TransactionDetailSerialize(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            item.stock = item.stock - request.data['quantity']
            item.balance = item.balance - (request.data['quantity'] * request.data['unit_price'])
            item.save()
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        except Transaction.DoesNotExist:
            raise NotFound

    @action(methods=['get'], detail=True, name='get detail sell')
    def get_detail_sell(self, request, *args, **kwargs):
        try:
            purchase_transaction = (Transaction
                                    .objects
                                    .filter(code=kwargs.get('code'), transaction_type='purchase')
                                    .values('code', 'date', 'description')
                                    .get())

            purchase_transaction_details = (TransactionDetail
                                            .objects
                                            .filter(header_code__code=kwargs.get('code'),
                                                    header_code__transaction_type='purchase')
                                            .values('item_code', 'quantity', 'unit_price', 'header_code')
                                            .all())

            purchase_transaction['details'] = purchase_transaction_details
            return Response(purchase_transaction, status=http_status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            raise NotFound
