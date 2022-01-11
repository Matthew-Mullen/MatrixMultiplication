from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4

# Create your models here.

class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'    

    @property
    def get_account(self):
        account = Account.objects.filter(userId=self).first()
        return account.id

    @property
    def get_account_github(self):
        account = Account.objects.filter(userId=self).first()
        return account.github
# Create your models here.
class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=uuid4, editable=False, unique=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    displayName = models.CharField(('displayName'), max_length=80, blank=True)
    money = models.IntegerField(default=0)

class StockOfPortfolio(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=uuid4, editable=False, unique=True)
    tag = models.CharField(primary_key=True, max_length=200, default=uuid4, editable=False, unique=True)
    quantityOwned=models.IntegerField(default=0)
    owner = ForeignKey(Account, on_delete=models.CASCADE)


