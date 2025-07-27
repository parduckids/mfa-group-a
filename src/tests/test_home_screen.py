from nicegui import ui
from nicegui.testing import User, Screen
import pytest
    
def test_splitter_initial(screen: Screen):
    screen.open('/')
    screen.should_contain('50')
    screen.should_contain('Agent Login')
    screen.should_contain('Username')
    screen.should_contain('Password')
    screen.find('Login')
    screen.should_contain('Flight Search ✈️')
    screen.should_contain('Welcome! Please provide the flight details.')
    screen.should_contain('Client ID')
    screen.should_contain('Flight Number')
    screen.find('Search')
    
def test_splitter_click_left(screen: Screen):
    screen.open('/')
    screen.should_contain('50')
    screen.find('Agent Login').click()
    screen.should_contain('90')
    
def test_splitter_click_right(screen: Screen):
    screen.open('/')
    screen.should_contain('50')
    screen.find('Flight Search ✈️').click()
    screen.should_contain('10')