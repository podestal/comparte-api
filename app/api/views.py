from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models
from . import serializers

class AccountOwnerViewSet(ModelViewSet):

    serializer_class = serializers.AccountOwnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.AccountOwner.objects.select_related('user')
        return models.AccountOwner.objects.none()
    
    @action(detail=False, methods=['get'], url_path='me')
    def get_balance_for_authenticated_user(self, request):
        owner, created = models.AccountOwner.objects.get_or_create(user=request.user)
        serializer = serializers.AccountOwnerSerializer(owner)
        return Response(serializer.data)

class ServiceViewSet(ModelViewSet):

    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class StreamingServiceAccountViewSet(ModelViewSet):

    queryset = models.StreamingServiceAccount.objects.all()
    serializer_class = serializers.StreamingServiceAccountSerializer

class ScreenSubscriptionViewSet(ModelViewSet):

    queryset = models.ScreenSubscription.objects.all()
    serializer_class = serializers.ScreenSubscriptionSerializer

class TransactionViewSet(ModelViewSet):

    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
