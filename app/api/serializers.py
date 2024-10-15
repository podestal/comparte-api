"""
API Serializers
"""

from rest_framework import serializers
from . import models


# class AccountOwnerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.AccountOwner
#         fields = ["id", "user", "balance"]


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = ["id", "name"]


class StreamingServiceAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StreamingServiceAccount
        fields = [
            "id",
            "service",
            "username",
            "password",
            "price_per_screen",
            "total_screens",
            "available_screens",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return models.StreamingServiceAccount.objects.create(owner=user, **validated_data)


class ScreenSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ScreenSubscription
        fields = [
            "id",
            "streaming_account",
            "user",
            "is_active",
            "subscription_date",
            "payment_status",
        ]


# class TransactionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Transaction
#         fields = ["id", "account_owner", "screen_subscription", "amount", "transaction_date"]
