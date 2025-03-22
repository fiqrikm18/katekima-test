from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Item


class ItemSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=100, required=True)
    unit = serializers.CharField(max_length=10, required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    stock = serializers.IntegerField(default=0, required=False)
    balance = serializers.IntegerField(default=0, required=False)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=['name'],
            )
        ]

    def create(self, validated_data):
        dict = {}
        dict['code'] = self.__generate_code()
        dict['name'] = validated_data.get('name')
        dict['unit'] = validated_data.get('unit')
        dict['description'] = validated_data.get('description')
        dict['stock'] = validated_data.get('stock')
        dict['balance'] = validated_data.get('balance')

        return Item.objects.create(**dict)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.unit = validated_data.get('unit')
        instance.description = validated_data.get('description')
        instance.stock = validated_data.get('stock')
        instance.balance = validated_data.get('balance')
        instance.save()
        return instance

    def __generate_code(self):
        code = 'I-'
        last_code = Item.objects.order_by('-id').values('code').first()
        if not last_code:
            return "I-001"

        splited_code = str.split(last_code['code'], '-')
        code += '{:03d}'.format(int(splited_code[len(splited_code) - 1]) + 1)
        return code
