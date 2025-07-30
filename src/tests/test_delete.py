import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import platform

mod = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

pytest_plugins = ['nicegui.testing.plugin']

@pytest.mark.module_under_test(startup)
def test_delete_client(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    button = screen.find_all_by_tag('button')
    button[0].click()
    screen.wait(0.5)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    screen.find('Delete')
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(1)
    screen.should_contain('Client not found')
    screen.wait(6) # wait for the notification to disappear
    
    inputs = screen.find_all_by_tag('input')
    
    def input_text(text):
        # Select the field and clear the content
        inputs[-1].click()
        inputs[-1].send_keys(mod + 'a')
        inputs[-1].send_keys(Keys.DELETE)
        
        # Add text
        inputs[-1].send_keys(text)
        
        # Click and wait 
        button_view[3].click()
        screen.wait(1)
    
    input_text(text='a')
    screen.should_contain('Client not found')
    screen.wait(6) # wait for the notification to disappear
    
    text = 5
    
    input_text(text)
    screen.should_not_contain('Client not found')    
    screen.find('Cancel').click()
    screen.wait(1)
    
    input_text(text)
    screen.find('Yes, delete').click()
    screen.should_contain(f'Are you sure you want to delete client {text} and all their flights?')
    screen.find('Yes, delete').click()
    screen.wait(1)
    screen.should_contain(f'Client {text} and all associated flights have been deleted')
    
@pytest.mark.module_under_test(startup)
def test_delete_airline(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    button = screen.find_all_by_tag('button')
    button[0].click()
    screen.wait(0.5)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    screen.find('Delete')
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(1)
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    inputs = screen.find_all_by_tag('input')
    
    def input_text(text):
        # Select the field and clear the content
        inputs[-1].click()
        inputs[-1].send_keys(mod + 'a')
        inputs[-1].send_keys(Keys.DELETE)
        
        # Add text
        inputs[-1].send_keys(text)
        
        # Click and wait 
        button_view[3].click()
        screen.wait(1)
    
    input_text(text='a')
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    text = 3
    
    input_text(text)
    screen.should_not_contain('Airline not found')    
    screen.find('Cancel').click()
    screen.wait(1)
    
    input_text(text)
    screen.find('Yes, delete').click()
    screen.should_contain(f'Are you sure you want to delete airline {text} and all associated flights?')
    screen.find('Yes, delete').click()
    screen.wait(1)
    screen.should_contain(f'Airline {text} and all associated flights have been deleted')
    
@pytest.mark.module_under_test(startup)
def test_delete_flight(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    button = screen.find_all_by_tag('button')
    button[0].click()
    screen.wait(0.5)
    
    # Flights tab
    screen.find('Flights').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    selects = screen.find_all_by_class('q-select')
    selects[0].click()
    screen.wait(0.5)
    
    options = screen.find_all_by_class('q-item')
    
    options[0].click()
    screen.wait(0.5)
    
    list_items = options = screen.find_all_by_class('q-list')
    list_items[-1].click()
    screen.wait(0.5)
    
    buttons = screen.find_all_by_class('q-btn')
    buttons[-1].click()
    screen.wait(0.5)
    screen.should_contain(f'Are you sure you want to delete this flight?')
    
    screen.find('Cancel').click()
    screen.wait(1)
    screen.should_not_contain(f'Are you sure you want to delete this flight?')
    
    buttons[-1].click()
    screen.wait(0.5)
    screen.find('Yes, delete').click()
