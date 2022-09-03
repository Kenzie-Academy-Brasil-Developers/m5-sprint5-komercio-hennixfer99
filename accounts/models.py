from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Accounts(AbstractUser):
    id = models.UUIDField(primary_key= True, editable = False, default = uuid.uuid4, unique= True)
    username = models.TextField(unique = True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False, blank=True, null = False)
    REQUIRED_FIELDS = ['first_name','last_name','is_seller']
   