import pytest
from nicegui.testing import User, Screen
from app.startup import startup

pytest_plugins = ['nicegui.testing.plugin']

@pytest.fixture
def user(user: User) -> User:
    #startup()
    return user

@pytest.fixture
def screen(screen: Screen) -> Screen:
    startup()
    return screen