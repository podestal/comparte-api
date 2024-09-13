"""
Urls for tracker api
"""

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('owners', views.AccountOwnerViewSet)
router.register('services', views.ServiceViewSet)
router.register('accounts', views.StreamingServiceAccountViewSet)
router.register('screens', views.ScreenSubscriptionViewSet)
router.register('transactions', views.TransactionViewSet)

urlpatterns = router.urls