import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import platform

mod = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

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
    inputs[-1].send_keys(mod + 'a')
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
    inputs[-1].send_keys(mod + 'a')
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
    inputs[-1].send_keys(mod + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    screen.wait(0.5)
    inputs[-1].send_keys('1')
    screen.wait(0.5)
    button_view[3].click()
    screen.should_not_contain('No data available')   
import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import mod, find_visible_buttons, get_highest_id_value, input_text
from pathlib import Path

@pytest.mark.order(15)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    texts = [
        'test name', 'test address', 'test city',
        'test zip code', 'test country', 'test phone number'
    ]
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.order(16)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    texts = ['test airline name']
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.order(17)
def test_view_flights_bookings(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Flights bookings tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    
    screen.find('View Bookings').click()
    screen.wait(0.5) 
    
    screen.should_contain('Booking ID')
    screen.should_contain('Flight ID')
    screen.should_not_contain('No data available')
        
@pytest.mark.order(18)
def test_view_available_flights(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Flights bookings tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('View Available Flight').click()
    screen.wait(0.5)
    
    texts = ['test start', 'test end']
    
    for text in texts:
        screen.should_contain(text) 
        
@pytest.mark.order(19)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # wait for the notification to disappear 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    clients_path = Path('src/data/clients.json')
    client_id = get_highest_id_value(clients_path, 'ID')
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   
    
@pytest.mark.order(20)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # wait for the notification to disappear 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    airlines_path = Path('src/data/airlines.json')
    airline_id = get_highest_id_value(airlines_path, 'ID')
    
    input_text(screen, airline_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   
 
@pytest.mark.order(21)
def test_view_flight_bookings_search(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Flights bookings tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    
    screen.find('View Bookings').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # wait for the notification to disappear 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    flights_bookings_path = Path('src/data/flights.json')
    flights_booking_id = get_highest_id_value(flights_bookings_path, 'Client_ID')
    
    input_text(screen, 1)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   

@pytest.mark.order(22)
def test_view_available_flights_search(screen: Screen):
    screen.open('/')
    
    # Expand the panel
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Flights bookings tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('View Available Flight').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # wait for the notification to disappear
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    available_flights_path = Path('src/data/available_flights.json')
    available_flights_id = get_highest_id_value(available_flights_path, 'Flight_ID')
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   