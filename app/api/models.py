"""
API Models
"""

from django.db import models
from django.conf import settings


class Service(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# class Balance(models.Model):
#     """Balance model"""

#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.amount


class StreamingServiceAccount(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    price_per_screen = models.DecimalField(max_digits=5, decimal_places=2)
    total_screens = models.PositiveIntegerField()
    available_screens = models.PositiveIntegerField()
    verfied = models.BooleanField(default=False)


class ScreenSubscription(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("N", "Not Initiated"),
        ("P", "Pending"),
        ("C", "Completed"),
    ]

    streaming_account = models.ForeignKey(
        StreamingServiceAccount, on_delete=models.CASCADE, related_name="screen"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="N")


# class Transaction(models.Model):

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     screen_subscription = models.ForeignKey(ScreenSubscription,
#  on_delete=models.CASCADE, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_date = models.DateTimeField(auto_now_add=True)
