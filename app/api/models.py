"""
API Models
"""

from django.db import models
from django.conf import settings

class Service(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AccountOwner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_owner')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class StreamingServiceAccount(models.Model):

    owner = models.ForeignKey(AccountOwner, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    price_per_screen = models.DecimalField(max_digits=5, decimal_places=2)
    total_screens = models.PositiveIntegerField()
    available_screens = models.PositiveIntegerField()

class ScreenSubscription(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]  

    streaming_account = models.ForeignKey(StreamingServiceAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    screen_number = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='P') 

class Transaction(models.Model):

    account_owner = models.ForeignKey(AccountOwner, on_delete=models.CASCADE)
    screen_subscription = models.ForeignKey(ScreenSubscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)