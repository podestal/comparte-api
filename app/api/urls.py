"""
Urls for tracker api
"""

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# router.register('owners', views.AccountOwnerViewSet, basename='owners')
router.register("services", views.ServiceViewSet, basename="services")
# router.register('accounts', views.StreamingServiceAccountViewSet, basename='accounts')
# router.register('screens', views.ScreenSubscriptionViewSet, basename='screens')
# router.register('transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = router.urls
