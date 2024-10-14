import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from api.models import Service
from core.models import User


@pytest.fixture
def api_client():
    """Fixture to provide APIClient instance."""
    return APIClient()


@pytest.fixture
def create_service():
    """Fixture to create a Service instance."""
    return baker.make(Service)


@pytest.fixture
def create_user():
    """Fixture to create a normal user."""
    return baker.make(User)


@pytest.fixture
def create_admin_user():
    """Fixture to create a admin."""
    return baker.make(User, is_staff=True)


@pytest.fixture
def authenticated_user(api_client, create_user):
    """Fixture to authenticate a normal user."""
    api_client.force_authenticate(user=create_user)
    return api_client


@pytest.fixture
def admin_user(api_client, create_admin_user):
    """Fixture to authenticate a admin user."""
    api_client.force_authenticate(user=create_admin_user)
    return api_client


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

    # Test create view (POST /services/) as an authenticated superuser
    def test_create_service(self, admin_user):
        service_data = {"name": "New Service"}
        response = admin_user.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Service.objects.filter(name="New Service").exists()

    # Test update view (PUT /services/{id}/) as an authenticated superuser
    def test_update_service(self, admin_user, create_service):
        updated_data = {"name": "Updated Service"}
        response = admin_user.put(f"/api/services/{create_service.id}/", updated_data)
        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Updated Service"

    # Test partial update view (PATCH /services/{id}/) as an authenticated superuser
    def test_partial_update_service(self, admin_user, create_service):
        response = admin_user.patch(
            f"/api/services/{create_service.id}/", {"name": "Partially Updated"}
        )
        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Partially Updated"

    # Test delete view (DELETE /services/{id}/) as an authenticated superuser
    def test_delete_service(self, admin_user, create_service):
        response = admin_user.delete(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Service.objects.filter(id=create_service.id).exists()

    # Test create service as an unauthenticated user
    def test_create_service_unauthenticated(self, authenticated_user):
        service_data = {"name": "Unauthorized Service"}
        response = authenticated_user.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test delete service as an unauthenticated user
    def test_delete_service_unauthenticated(self, create_service, authenticated_user):
        response = authenticated_user.delete(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
