import pytest
from rest_framework import status
from model_bakery import baker
from api.models import ScreenSubscription, StreamingServiceAccount, Service


@pytest.fixture
def create_service():
    """Fixture to create a Service instance."""
    return baker.make(Service)


@pytest.fixture
def create_streaming_service_account(create_user, create_service):
    """Fixture to create a StreamingServiceAccount instance."""
    return baker.make(
        StreamingServiceAccount,
        owner=create_user,
        service=create_service,
        username="testuser",
        password="password123",
        price_per_screen=9.99,
        total_screens=4,
        available_screens=2,
    )


@pytest.fixture
def create_screen_subscription(create_user, create_streaming_service_account):
    """Fixture to create a ScreenSubscription instance."""
    return baker.make(
        ScreenSubscription,
        streaming_account=create_streaming_service_account,
        user=None,  # Initially, no user is assigned
        is_active=True,
        payment_status="P",
    )


@pytest.mark.django_db
class TestScreenSubscription:

    def test_list_screens_unauthenticated_return_200(self, api_client, create_screen_subscription):
        response = api_client.get("/api/screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["streaming_account"] == create_screen_subscription.streaming_account.id
        )

    def test_get_queryset_no_active_screens_unauthenticated_return_200(self, api_client):

        response = api_client.get("/api/screens/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_get_queryset_multiple_accounts_unauthenticated_return_200(self, api_client):
        account_1 = baker.make(StreamingServiceAccount, total_screens=4)
        account_2 = baker.make(StreamingServiceAccount, total_screens=2)

        baker.make(
            ScreenSubscription, streaming_account=account_1, is_active=True, user=None, _quantity=3
        )
        baker.make(
            ScreenSubscription, streaming_account=account_2, is_active=True, user=None, _quantity=1
        )

        response = api_client.get("/api/screens/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Only account_2 has the least available screens
        assert response.data[0]["streaming_account"] == account_2.id

    def test_get_queryset_minimum_screens_unauthenticated_return_200(self, api_client):

        account_1 = baker.make(StreamingServiceAccount, total_screens=4)
        account_2 = baker.make(StreamingServiceAccount, total_screens=4)

        baker.make(
            ScreenSubscription, streaming_account=account_1, is_active=True, user=None, _quantity=2
        )
        baker.make(
            ScreenSubscription, streaming_account=account_2, is_active=True, user=None, _quantity=3
        )

        response = api_client.get("/api/screens/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Only account_1 should be returned
        assert response.data[0]["streaming_account"] == account_1.id

    def test_list_screens_authenticated_return_200(
        self, authenticated_user, create_screen_subscription
    ):
        response = authenticated_user.get("/api/screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["streaming_account"] == create_screen_subscription.streaming_account.id
        )

    def test_list_screens_admin_return_200(self, admin_user, create_screen_subscription):
        response = admin_user.get("/api/screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["streaming_account"] == create_screen_subscription.streaming_account.id
        )

    def test_retrieve_screen_subscription_unauthenticated_return_200(
        self, api_client, create_screen_subscription
    ):
        response = api_client.get(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["streaming_account"] == create_screen_subscription.streaming_account.id

    def test_retrieve_screen_subscription_authenticated_return_200(
        self, authenticated_user, create_screen_subscription
    ):
        response = authenticated_user.get(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["streaming_account"] == create_screen_subscription.streaming_account.id

    def test_retrieve_screen_subscription_admin_return_200(
        self, admin_user, create_screen_subscription
    ):
        response = admin_user.get(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["streaming_account"] == create_screen_subscription.streaming_account.id

    def test_my_screens_unauthenticated_return_empty(self, api_client):
        response = api_client.get("/api/screens/my_screens/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_my_screens_authenticated_no_screens_return_empty(self, authenticated_user):
        response = authenticated_user.get("/api/screens/my_screens/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_my_screens_authenticated_with_screens_return_data(
        self, authenticated_user, create_user
    ):
        streaming_account = baker.make(StreamingServiceAccount)
        baker.make(
            ScreenSubscription,
            user=create_user,
            streaming_account=streaming_account,
            is_active=True,
        )

        response = authenticated_user.get("/api/screens/my_screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["streaming_account"] == streaming_account.id

    def test_my_screens_authenticated_multiple_screens_return_data(
        self, authenticated_user, create_user
    ):

        streaming_account_1 = baker.make(StreamingServiceAccount)
        streaming_account_2 = baker.make(StreamingServiceAccount)

        baker.make(
            ScreenSubscription,
            user=create_user,
            streaming_account=streaming_account_1,
            is_active=True,
        )
        baker.make(
            ScreenSubscription,
            user=create_user,
            streaming_account=streaming_account_2,
            is_active=True,
        )

        response = authenticated_user.get("/api/screens/my_screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["streaming_account"] == streaming_account_1.id
        assert response.data[1]["streaming_account"] == streaming_account_2.id

    def test_create_screen_subscription_unauthenticated_return_401(
        self, api_client, create_streaming_service_account
    ):
        screen_data = {
            "streaming_account": create_streaming_service_account.id,
        }
        response = api_client.post("/api/screens/", screen_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_screen_subscription_authenticated_return_403(
        self, authenticated_user, create_streaming_service_account
    ):
        screen_data = {
            "streaming_account": create_streaming_service_account.id,
        }
        response = authenticated_user.post("/api/screens/", screen_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_screen_subscription_admin_return_201(
        self, admin_user, create_streaming_service_account
    ):
        screen_data = {
            "streaming_account": create_streaming_service_account.id,
        }
        response = admin_user.post("/api/screens/", screen_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ScreenSubscription.objects.filter(
            streaming_account=create_streaming_service_account
        ).exists()

    def test_partial_update_screen_subscription_unauthenticated_return_401(
        self, api_client, create_screen_subscription
    ):
        response = api_client.patch(
            f"/api/screens/{create_screen_subscription.id}/",
            {"payment_status": "C"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_screen_subscription_authenticated_return_200(
        self, authenticated_user, create_screen_subscription
    ):
        response = authenticated_user.patch(
            f"/api/screens/{create_screen_subscription.id}/",
            {"payment_status": "C"},
        )
        assert response.status_code == status.HTTP_200_OK
        create_screen_subscription.refresh_from_db()
        assert create_screen_subscription.payment_status == "C"

    def test_partial_update_screen_subscription_admin_return_200(
        self, admin_user, create_screen_subscription
    ):
        response = admin_user.patch(
            f"/api/screens/{create_screen_subscription.id}/",
            {"payment_status": "C"},
        )
        assert response.status_code == status.HTTP_200_OK
        create_screen_subscription.refresh_from_db()
        assert create_screen_subscription.payment_status == "C"

    def test_delete_screen_subscription_unauthenticated_return_401(
        self, api_client, create_screen_subscription
    ):
        response = api_client.delete(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_screen_subscription_authenticated_return_204(
        self, authenticated_user, create_screen_subscription
    ):
        response = authenticated_user.delete(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_screen_subscription_admin_return_204(
        self, admin_user, create_screen_subscription
    ):
        response = admin_user.delete(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ScreenSubscription.objects.filter(id=create_screen_subscription.id).exists()
