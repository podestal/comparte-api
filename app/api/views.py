from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers

class AccountOwnerViewSet(ModelViewSet):

    queryset = models.AccountOwner.objects.all()
    serializer_class = serializers.AccountOwnerSerializer


