import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from api.models import Service
from core.models import User


@pytest.fixture
def api_client():
    return APIClient(User)


@pytest.fixture
def create_service():
    return baker.make(Service)


@pytest.fixture
def authenticated_user(api_client, create_user):
    """Fixture to authenticate a user."""
    api_client.force_authenticate(user=create_user)
    return create_user


@pytest.fixture
def create_superuser():
    """Fixture to create a superuser."""
    return baker.make(User, is_superuser=True)


@pytest.fixture
def authenticated_superuser(api_client, create_superuser):
    """Fixture to authenticate a superuser."""
    api_client.force_authenticate(user=create_superuser)
    return create_superuser


@pytest.mark.django_db
class TestServiceViewSet:

    # Test list view (GET /services/)
    def test_list_services(self, api_client, create_service):
        response = api_client.get("/api/services/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_service.name

    # Test retrieve view (GET /services/{id}/)
    def test_retrieve_service(self, api_client, create_service):
        response = api_client.get(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == create_service.name

    # Test create view (POST /services/)
    def test_create_service(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        service_data = {"name": "New Service"}
        response = api_client.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Service.objects.filter(name="New Service").exists()

    # Test update view (PUT /services/{id}/)
    def test_update_service(self, api_client, create_service, admin_user):
        api_client.force_authenticate(user=admin_user)
        updated_data = {"name": "Updated Service"}
        response = api_client.put(f"/api/services/{create_service.id}/", updated_data)

        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Updated Service"

    # # Test partial update view (PATCH /services/{id}/)
    def test_partial_update_service(self, api_client, create_service, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            f"/api/services/{create_service.id}/", {"name": "Partially Updated"}
        )

        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Partially Updated"

    # # Test delete view (DELETE /services/{id}/)
    def test_delete_service(self, api_client, create_service, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f"/api/services/{create_service.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Service.objects.filter(id=create_service.id).exists()

    # # Test permissions for unauthenticated users (POST)
    def test_create_service_unauthenticated(self, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user=user)
        service_data = {"name": "Unauthorized Service"}
        response = api_client.post("/api/services/", service_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # # Test permissions for unauthenticated users (DELETE)
    def test_delete_service_unauthenticated(self, api_client, create_service):
        user = baker.make(User)
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/services/{create_service.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
