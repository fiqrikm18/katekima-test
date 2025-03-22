from django.db import models

from libs.models import SoftDeleteBaseModel

TRANSACTION_TYPE = [
    ('sell', 'Sell'),
    ('purchase', 'Purchase'),
]


# Create your models here.
class Transaction(SoftDeleteBaseModel.SoftDeleteBaseModel):
    code = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    description = models.TextField()
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, default='purchase')

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return self.code


class TransactionDetail(SoftDeleteBaseModel.SoftDeleteBaseModel):
    item_code = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    unit_price = models.IntegerField(default=0)
    header_code = models.ForeignKey(Transaction, on_delete=models.CASCADE, to_field='code', db_column='header_code')

    class Meta:
        db_table = 'transaction_details'

    def __str__(self):
        return self.header_code
