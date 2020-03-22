import pytest
import uuid
from pytest_factoryboy import register

from boards.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def steve(db, user_factory):
    return user_factory(username="steve")


@pytest.fixture
def amy(db, user_factory):
    return user_factory(username="amy")


@pytest.fixture
def leo(db, user_factory):
    return user_factory(username="leo")