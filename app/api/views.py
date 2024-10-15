from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.db.models import Count, Q, Min

# from rest_framework.decorators import action
# from rest_framework.response import Response
from . import models
from . import serializers


# class AccountOwnerViewSet(ModelViewSet):

#     serializer_class = serializers.AccountOwnerSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return models.AccountOwner.objects.select_related('user')
#         return models.AccountOwner.objects.none()

#     @action(detail=False, methods=['get'], url_path='me')
#     def get_balance_for_authenticated_user(self, request):
#         owner, created = models.AccountOwner.objects.get_or_create(user=request.user)
#         serializer = serializers.AccountOwnerSerializer(owner)
#         return Response(serializer.data)


class ServiceViewSet(ModelViewSet):

    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class StreamingServiceAccountViewSet(ModelViewSet):

    queryset = models.StreamingServiceAccount.objects.select_related("owner", "service")
    serializer_class = serializers.StreamingServiceAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(owner=self.request.user)


class ScreenSubscriptionViewSet(ModelViewSet):

    queryset = models.ScreenSubscription.objects.select_related("streaming_account", "user")
    serializer_class = serializers.ScreenSubscriptionSerializer

    def get_queryset(self):
        accounts_with_available_screens = models.StreamingServiceAccount.objects.annotate(
            available_screens_count=Count(
                "screen",
                filter=Q(screen__is_active=True, screen__user__isnull=True),
            )
        )

        min_available_screens = accounts_with_available_screens.aggregate(
            min_screens=Min("available_screens_count")
        )["min_screens"]

        accounts_with_least_available_screens = accounts_with_available_screens.filter(
            available_screens_count=min_available_screens
        ).values_list("id", flat=True)

        available_screens = (
            models.ScreenSubscription.objects.filter(
                is_active=True,
                user__isnull=True,
                streaming_account__in=accounts_with_least_available_screens,
            )
            .order_by("streaming_account")  # Order to get the first available one
            .distinct("streaming_account")  # Get one screen per streaming account
        )

        return available_screens


# class TransactionViewSet(ModelViewSet):

#     queryset = models.Transaction.objects.all()
#     serializer_class = serializers.TransactionSerializer
