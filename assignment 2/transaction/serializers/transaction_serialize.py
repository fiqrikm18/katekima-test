import datetime

from rest_framework import serializers

from ..models import Transaction, TransactionDetail


class TransactionDetailSerialize(serializers.Serializer):
    item_code = serializers.CharField(max_length=10, required=True)
    quantity = serializers.IntegerField(default=0)
    unit_price = serializers.IntegerField(default=0)
    header_code = serializers.CharField(required=True)

    def create(self, validated_data):
        dict = {}
        transaction = Transaction.objects.filter(code=validated_data.get('header_code')).first()
        dict['item_code'] = validated_data.get('item_code')
        dict['quantity'] = validated_data.get('quantity')
        dict['unit_price'] = validated_data.get('unit_price')
        dict['header_code'] = transaction

        return TransactionDetail.objects.create(**dict)

    def update(self, instance, validated_data):
        instance.item_code = validated_data.get('item_code')
        instance.quantity = validated_data.get('quantity')
        instance.unit_price = validated_data.get('unit_price')
        instance.header_code = validated_data.get('header_code')
        instance.save()
        return instance


class TransactionSerialize(serializers.Serializer):
    code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date = serializers.DateField(required=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    transaction_type = serializers.CharField(required=False)

    def create(self, validated_data):
        dict = {}
        dict['code'] = self.__generate_code()
        dict['date'] = datetime.date.today().isoformat() if validated_data.get('date') is None else validated_data.get('date')
        dict['description'] = validated_data.get('description')
        dict['transaction_type'] = validated_data.get('transaction_type')
        return Transaction.objects.create(**dict)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description')
        instance.save()
        return instance

    def __generate_code(self):
        code = 'P-'
        last_code = Transaction.objects.order_by('-id').values('code').first()
        if not last_code:
            return "P-001"

        splited_code = str.split(last_code['code'], '-')
        code += '{:03d}'.format(int(splited_code[len(splited_code) - 1]) + 1)
        return code
