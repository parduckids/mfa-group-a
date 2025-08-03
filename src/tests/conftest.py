import pytest
from nicegui.testing import Screen
from app.startup import startup

# Register the NiceGUI test plugin for pytest
pytest_plugins = ['nicegui.testing.plugin']

@pytest.fixture
def screen(screen: Screen) -> Screen:
    """
    Pytest fixture that initializes the NiceGUI test screen.

    This fixture runs the application startup process and returns a
    configured Screen object for use in UI tests.

    Returns:
        Screen: An instance of NiceGUI's testing Screen with the app initialized.
    """
    startup()
    return screen