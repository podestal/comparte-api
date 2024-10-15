import pytest
from rest_framework import status
from model_bakery import baker
from api.models import StreamingServiceAccount, Service


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


@pytest.mark.django_db
class TestStreamingServiceAccount:

    def test_list_streaming_accounts_unauthenticated_return_401(
        self, api_client, create_streaming_service_account
    ):
        response = api_client.get("/api/accounts/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_streaming_accounts_authenticated_return_200(
        self, authenticated_user, create_streaming_service_account
    ):
        response = authenticated_user.get("/api/accounts/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["username"] == create_streaming_service_account.username

    def test_retrieve_streaming_account_authenticated_return_200(
        self, authenticated_user, create_streaming_service_account
    ):
        response = authenticated_user.get(f"/api/accounts/{create_streaming_service_account.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == create_streaming_service_account.username

    def test_retrieve_streaming_account_unauthenticated_return_401(
        self, api_client, create_streaming_service_account
    ):
        response = api_client.get(f"/api/accounts/{create_streaming_service_account.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_streaming_account_unauthenticated_return_401(
        self, api_client, create_user, create_service
    ):
        account_data = {
            "service": create_service.id,
            "username": "newuser",
            "password": "password123",
            "price_per_screen": 9.99,
            "total_screens": 4,
            "available_screens": 2,
        }
        response = api_client.post("/api/accounts/", account_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_streaming_account_authenticated_return_201(
        self, authenticated_user, create_user, create_service
    ):
        account_data = {
            "service": create_service.id,
            "username": "newuser",
            "password": "password123",
            "price_per_screen": 9.99,
            "total_screens": 4,
            "available_screens": 2,
        }
        response = authenticated_user.post("/api/accounts/", account_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert StreamingServiceAccount.objects.filter(username="newuser").exists()

    def test_update_streaming_account_unauthenticated_return_401(
        self, api_client, create_streaming_service_account
    ):
        updated_data = {"username": "updateduser"}
        response = api_client.patch(
            f"/api/accounts/{create_streaming_service_account.id}/", updated_data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_streaming_account_authenticated_return_200(
        self, authenticated_user, create_streaming_service_account
    ):
        updated_data = {"username": "updateduser"}
        response = authenticated_user.patch(
            f"/api/accounts/{create_streaming_service_account.id}/", updated_data
        )
        assert response.status_code == status.HTTP_200_OK
        create_streaming_service_account.refresh_from_db()
        assert create_streaming_service_account.username == "updateduser"

    def test_delete_streaming_account_unauthenticated_return_401(
        self, api_client, create_streaming_service_account
    ):
        response = api_client.delete(f"/api/accounts/{create_streaming_service_account.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_streaming_account_authenticated_return_204(
        self, authenticated_user, create_streaming_service_account
    ):
        response = authenticated_user.delete(
            f"/api/accounts/{create_streaming_service_account.id}/"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not StreamingServiceAccount.objects.filter(
            id=create_streaming_service_account.id
        ).exists()
