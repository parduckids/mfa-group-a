import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import platform

mod = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

pytest_plugins = ['nicegui.testing.plugin']

@pytest.mark.module_under_test(startup)
def test_edit_client(screen: Screen):
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
    
    screen.find('Edit').click()
    screen.wait(6)
    
    screen.find('Edit')
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
    
    input_text(text='5')
    screen.should_not_contain('Client not found')
    screen.should_contain('Edit Client ID:')
    
    screen.find('Cancel').click()
    screen.wait(1)
    
    input_text(text='5')
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    screen.find('Save Changes').click()
    screen.wait(1)
    screen.should_contain('Client updated successfully')
    
@pytest.mark.module_under_test(startup)
def test_edit_airline(screen: Screen):
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
    
    screen.find('Edit').click()
    screen.wait(6)
    
    screen.find('Edit')
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
    
    input_text(text='3')
    screen.should_not_contain('Airline not found')
    screen.should_contain('Edit Airline ID:')
    
    screen.find('Cancel').click()
    screen.wait(1)
    
    input_text(text='3')
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Company Name"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    screen.find('Save Changes').click()
    screen.wait(1)
    screen.should_contain('Airline updated successfully')
    
@pytest.mark.module_under_test(startup)
def test_edit_flight(screen: Screen):
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
    
    screen.find('Edit').click()
    screen.wait(6)
    
    screen.find('Edit')
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(1)
    screen.should_contain('Flight not found')
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
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(text='3')
    screen.should_not_contain('Flight not found')
    screen.should_contain('Edit Flight for Client ID:')
    
    screen.find('Cancel').click()
    screen.wait(1)
    
    input_text(text='3')
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Start City"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    screen.find('Save Changes').click()
    screen.wait(1)
    screen.should_contain('Flight updated successfully')