import pytest
from rest_framework import status
from model_bakery import baker
from api.models import Service


@pytest.fixture
def create_service():
    """Fixture to create a Service instance."""
    return baker.make(Service)


@pytest.mark.django_db
class TestService:

    def test_list_services_unauthenticated_return_200(self, api_client, create_service):
        response = api_client.get("/api/services/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_service.name

    def test_list_services_authenticated_return_200(self, authenticated_user, create_service):
        response = authenticated_user.get("/api/services/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_service.name

    def test_list_services_admin_return_200(self, admin_user, create_service):
        response = admin_user.get("/api/services/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_service.name

    def test_retrieve_service(self, api_client, create_service):
        response = api_client.get(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == create_service.name

    def test_create_service_unauthenticated_return_401(self, api_client):
        service_data = {"name": "Unauthorized Service"}
        response = api_client.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_service_authenticated_return_403(self, authenticated_user):
        service_data = {"name": "Unauthorized Service"}
        response = authenticated_user.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_service(self, admin_user):
        service_data = {"name": "New Service"}
        response = admin_user.post("/api/services/", service_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Service.objects.filter(name="New Service").exists()

    def test_update_service_unauthenticated_return_401(self, api_client, create_service):
        updated_data = {"name": "Updated Service"}
        response = api_client.put(f"/api/services/{create_service.id}/", updated_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_service_authenticated_return_401(self, authenticated_user, create_service):
        updated_data = {"name": "Updated Service"}
        response = authenticated_user.put(f"/api/services/{create_service.id}/", updated_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_service_admin_return_200(self, admin_user, create_service):
        updated_data = {"name": "Updated Service"}
        response = admin_user.put(f"/api/services/{create_service.id}/", updated_data)
        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Updated Service"

    def test_partial_update_service_unauthenticated_return_401(self, api_client, create_service):
        response = api_client.patch(
            f"/api/services/{create_service.id}/", {"name": "Partially Updated"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_service_authenticated_return_403(
        self, authenticated_user, create_service
    ):
        response = authenticated_user.patch(
            f"/api/services/{create_service.id}/", {"name": "Partially Updated"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_partial_update_service_admin_return_200(self, admin_user, create_service):
        response = admin_user.patch(
            f"/api/services/{create_service.id}/", {"name": "Partially Updated"}
        )
        assert response.status_code == status.HTTP_200_OK
        create_service.refresh_from_db()
        assert create_service.name == "Partially Updated"

    def test_delete_service_unauthenticated_return_401(self, create_service, api_client):
        response = api_client.delete(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_service_authenticated_return_403(self, create_service, authenticated_user):
        response = authenticated_user.delete(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_service_admin_return_204(self, admin_user, create_service):
        response = admin_user.delete(f"/api/services/{create_service.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Service.objects.filter(id=create_service.id).exists()
