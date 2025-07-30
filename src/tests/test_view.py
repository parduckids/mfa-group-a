import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

pytest_plugins = ['nicegui.testing.plugin']

@pytest.mark.module_under_test(startup)
def test_view_client(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    texts = [
        'test name', 'test address', '', '', 'test city', '',
        'test zip code', 'test country', 'test phone number'
    ]
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.module_under_test(startup)
def test_view_airline(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    texts = ['test airline name']
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.module_under_test(startup)
def test_view_flight(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    texts = ['test start', 'test end']
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.module_under_test(startup)
def test_view_client_search(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    inputs = screen.find_all_by_tag('input')
    inputs[-1].send_keys('a')
    screen.wait(6)
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    inputs[-1].click()
    inputs[-1].send_keys(Keys.CONTROL + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    screen.wait(0.5)
    inputs[-1].send_keys('1')
    screen.wait(0.5)
    button_view[3].click()
    screen.should_not_contain('No data available')   
    
@pytest.mark.module_under_test(startup)
def test_view_airline_search(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    inputs = screen.find_all_by_tag('input')
    inputs[-1].send_keys('a')
    screen.wait(6)
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    inputs[-1].click()
    inputs[-1].send_keys(Keys.CONTROL + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    screen.wait(0.5)
    inputs[-1].send_keys('1')
    screen.wait(0.5)
    button_view[3].click()
    screen.should_not_contain('No data available')   
 
@pytest.mark.module_under_test(startup)
def test_view_flight_search(screen: Screen):
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
    
    screen.find('View').click()
    screen.wait(0.5)
    
    inputs = screen.find_all_by_tag('input')
    inputs[-1].send_keys('a')
    screen.wait(6)
    button_view = screen.find_all_by_tag('button')
    button_view[3].click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    inputs[-1].click()
    inputs[-1].send_keys(Keys.CONTROL + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    screen.wait(0.5)
    inputs[-1].send_keys('1')
    screen.wait(0.5)
    button_view[3].click()
    screen.should_not_contain('No data available')   
