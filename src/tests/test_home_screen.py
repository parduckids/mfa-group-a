from nicegui import ui
from nicegui.testing import Screen
import pytest
    
@pytest.mark.order(4)
def test_splitter_initial(screen: Screen):
    """
    Verifies the initial state of the splitter layout on application load.

    This test checks that:
        - The initial width of both panels is set to 50%
        - All expected UI elements are visible, including login and search fields

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    screen.open('/')
    
    # Check the initial screen width
    width_home = screen.find_by_class('splitter-value')
    text_home = width_home.get_attribute('textContent').strip()
    assert '50' in text_home
    
    # Check for all necessary texts
    screen.should_contain('Agent Login')
    screen.should_contain('Username')
    screen.should_contain('Password')
    screen.find('Login')
    screen.should_contain('Flight Search ✈️')
    screen.should_contain('Welcome! Please provide the flight details.')
    screen.should_contain('Client ID')
    screen.find('Search')
    
@pytest.mark.order(5)
def test_splitter_click_left(screen: Screen):
    """
    Verifies the splitter behavior when the left panel (Agent Login) is clicked.

    This test checks that:
        - The initial width is 50%
        - Clicking the left panel expands it to 90% width

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    screen.open('/')
    
    # Check the initial screen width
    width_home = screen.find_by_class('splitter-value')
    text_home = width_home.get_attribute('textContent').strip()
    assert '50' in text_home
    
    # Click on the left side and wait for update
    screen.find('Agent Login').click()
    screen.wait(1)
    
    # Check the updated screen width
    width_before = screen.find_by_class('splitter-value-before')
    text_before = width_before.get_attribute('textContent').strip()
    assert '90' in text_before
    
@pytest.mark.order(6)
def test_splitter_click_right(screen: Screen):
    """
    Verifies the splitter behavior when the right panel (Flight Search) is clicked.

    This test checks that:
        - The initial width is 50%
        - Clicking the right panel shrinks it to 10% width

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    screen.open('/')
    
    # Check the initial screen width
    width_home = screen.find_by_class('splitter-value')
    text_home = width_home.get_attribute('textContent').strip()
    assert '50' in text_home
    
    # Click on the right side and wait for update
    screen.find('Flight Search ✈️').click()
    screen.wait(1)
    
    # Check the updated screen width
    width_after = screen.find_by_class('splitter-value-after')
    text_after = width_after.get_attribute('textContent').strip()
    assert '10' in text_after