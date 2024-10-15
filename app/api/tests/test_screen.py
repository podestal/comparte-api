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
class TestScreenSubscriptionViewSet:
    # Test list view (GET /screens/)
    def test_list_screens(self, authenticated_user, create_screen_subscription):
        response = authenticated_user.get("/api/screens/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["streaming_account"] == create_screen_subscription.streaming_account.id
        )

    # Test retrieve view (GET /screens/{id}/)
    def test_retrieve_screen_subscription(self, authenticated_user, create_screen_subscription):
        response = authenticated_user.get(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["streaming_account"] == create_screen_subscription.streaming_account.id

    # Test create view (POST /screens/) as an authenticated user
    def test_create_screen_subscription(self, admin_user, create_streaming_service_account):
        screen_data = {
            "streaming_account": create_streaming_service_account.id,
        }
        response = admin_user.post("/api/screens/", screen_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ScreenSubscription.objects.filter(
            streaming_account=create_streaming_service_account
        ).exists()

    # Test partial update view (PATCH /screens/{id}/)
    def test_partial_update_screen_subscription(
        self, authenticated_user, create_screen_subscription
    ):
        response = authenticated_user.patch(
            f"/api/screens/{create_screen_subscription.id}/",
            {"payment_status": "C"},
        )
        assert response.status_code == status.HTTP_200_OK
        create_screen_subscription.refresh_from_db()
        assert create_screen_subscription.payment_status == "C"

    # Test delete view (DELETE /screens/{id}/)
    def test_delete_screen_subscription(self, admin_user, create_screen_subscription):
        response = admin_user.delete(f"/api/screens/{create_screen_subscription.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ScreenSubscription.objects.filter(id=create_screen_subscription.id).exists()
