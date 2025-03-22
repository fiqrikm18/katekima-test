from django.db import models

from libs.models.SoftDeleteBaseModel import SoftDeleteBaseModel

ITEM_UNIT = [
    ('pcs', 'Pcs'),
]


# Create your models here.
class Item(SoftDeleteBaseModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10, choices=ITEM_UNIT)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name
