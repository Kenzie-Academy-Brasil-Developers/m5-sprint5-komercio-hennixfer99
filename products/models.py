from django.db import models
import uuid

class Products(models.Model):
    id = models.UUIDField(primary_key= True, editable = False, default = uuid.uuid4, unique= True)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)
    seller = models.ForeignKey('accounts.Accounts', on_delete = models.CASCADE, related_name = 'product')
