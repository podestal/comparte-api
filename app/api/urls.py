"""
Urls for tracker api
"""

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('account_owners', views.AccountOwnerViewSet)

urlpatterns = router.urls