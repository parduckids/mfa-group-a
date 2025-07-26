import pytest
from nicegui.testing import User
from app.startup import startup

pytest_plugins = ['nicegui.testing.user_plugin']

@pytest.fixture
def user(user: User) -> User:
    startup()
    return user