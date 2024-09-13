from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers

class AccountOwnerViewSet(ModelViewSet):

    queryset = models.AccountOwner.objects.all()
    serializer_class = serializers.AccountOwnerSerializer

class ServiceViewSet(ModelViewSet):

    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class StreamingServiceAccountViewSet(ModelViewSet):

    queryset = models.StreamingServiceAccount.objects.all()
    serializer_class = serializers.StreamingServiceAccountSerializer

class ScreenSubscriptionViewSet(ModelViewSet):

    queryset = models.ScreenSubscription.objects.all()
    serializer_class = serializers.ScreenSubscriptionSerializer

class TransactionViewSet(ModelViewSet):

    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
