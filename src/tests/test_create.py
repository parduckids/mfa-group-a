import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

pytest_plugins = ['nicegui.testing.plugin']

@pytest.mark.module_under_test(startup)
def test_create_client(screen: Screen):
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
    
    screen.find('Create').click()
    screen.wait(0.5)
    
    def complete_fields(names, texts):
        if isinstance(names, str):
            names = [names]
        if isinstance(texts, str):
            texts = [texts] * len(names)
            
        for name, text in zip(names, texts):
            input_element = screen.selenium.find_element(By.XPATH, f'//*[@aria-label="{name.title()}"]')
            for char in text:
                input_element.send_keys(char)
                screen.wait(0.1)
        
    names = [
        'Name', 'Address Line 1', 'Address Line 2',
        'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
        'Phone Number'
    ]
    texts = [
        'test name', 'test address', '', '', 'test city', '',
        'test zip code', 'test country', 'test phone number'
    ]
        
    # Input the data fields for creating the client
    complete_fields(names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')

    # Ensure client is created and the tab has been changed
    screen.find('Create Client').click()
    screen.wait(1)
    screen.should_contain('Client created with ID')
    screen.should_not_contain('Create Client')
    
@pytest.mark.module_under_test(startup)
def test_create_airline(screen: Screen):
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
    
    screen.find('Create').click()
    screen.wait(0.5)
    
    def complete_fields(names, texts):
        if isinstance(names, str):
            names = [names]
        if isinstance(texts, str):
            texts = [texts] * len(names)
            
        for name, text in zip(names, texts):
            input_element = screen.selenium.find_element(By.XPATH, f'//*[@aria-label="{name.title()}"]')
            for char in text:
                input_element.send_keys(char)
                screen.wait(0.1)
        
    names = ['Company Name']
    texts = ['test airline name']
        
    # Input the data fields for creating the client
    complete_fields(names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')

    # Ensure airline is created and the tab has been changed
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    screen.find('Create Airline').click()
    screen.wait(1)
    screen.should_contain('Airline created with ID')
    screen.should_not_contain('Create Airline')
    
@pytest.mark.module_under_test(startup)
def test_create_flight(screen: Screen):
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
    
    screen.find('Create').click()
    screen.wait(0.5)
    
    def complete_fields(names, texts):
        if isinstance(names, str):
            names = [names]
        if isinstance(texts, str):
            texts = [texts] * len(names)
            
        for name, text in zip(names, texts):
            input_element = screen.selenium.find_element(By.XPATH, f'//*[@aria-label="{name.title()}"]')
            for char in text:
                input_element.send_keys(char)
                screen.wait(0.1)

    selects = screen.find_all_by_class('q-select')
    
    for s in selects:
        s.click()
        screen.wait(0.5)
        options = screen.find_all_by_class('q-item')
        options[0].click()
        screen.wait(0.5)
    
    names = ['Start City', 'End City']
    texts = ['test start', 'test end']
        
    # Input the data fields for creating the client
    complete_fields(names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')
    
    # Use default for the date field

    # Ensure flight is created and the tab has been changed
    screen.find('Create Flight').click()
    screen.wait(1)
    screen.should_contain('Flight created')
    screen.should_not_contain('Create Flight')