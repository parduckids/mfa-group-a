from nicegui import ui
from nicegui.testing import User, Screen
import pytest
    
def test_splitter_initial(screen: Screen):
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
    
def test_splitter_click_left(screen: Screen):
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
    
def test_splitter_click_right(screen: Screen):
    screen.open('/')
    
    # Check the initial screen width
    width_home = screen.find_by_class('splitter-value')
    text_home = width_home.get_attribute('textContent').strip()
    assert '50' in text_home
    
    # Click on the left side and wait for update
    screen.find('Flight Search ✈️').click()
    screen.wait(1)
    
    # Check the updated screen width
    width_after = screen.find_by_class('splitter-value-after')
    text_after = width_after.get_attribute('textContent').strip()
    assert '10' in text_after