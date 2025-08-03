import pytest
from nicegui.testing import Screen
from app.startup import startup

pytest_plugins = ['nicegui.testing.plugin']

@pytest.fixture
def screen(screen: Screen) -> Screen:
    startup()
    return screen