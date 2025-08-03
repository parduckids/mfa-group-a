import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons, complete_fields

@pytest.mark.order(11)
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
    buttons_login = screen.find_all_by_tag('button')
    visible_buttons_login = [btn for btn in buttons_login if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('Create').click()
    screen.wait(6)
        
    names = [
        'Name', 'Address Line 1', 'Address Line 2',
        'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
        'Phone Number'
    ]
    texts = [
        'test name', 'test address', '', '', 'test city', '',
        'test zip code', 'test country', 'test phone number'
    ]
        
    create_client = find_visible_buttons(screen)
    visible_buttons_create_client = [btn for btn in create_client if btn.is_displayed()]
    next(b for b in visible_buttons_create_client if b.text == 'CREATE CLIENT').click()
    screen.should_contain('Please fill in all required fields.')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
        
    # Input the data fields for creating the client
    complete_fields(screen, names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')

    # Ensure client is created and the tab has been changed
    next(b for b in visible_buttons_create_client if b.text == 'CREATE CLIENT').click()
    screen.wait(1)
    screen.should_contain('Client created with ID')
    
@pytest.mark.order(12)
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
    buttons_login = screen.find_all_by_tag('button')
    visible_buttons_login = [btn for btn in buttons_login if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(6)
    
    screen.find('Create').click()
    screen.wait(1)
    
    create_airline = find_visible_buttons(screen)
    visible_buttons_create_airline = [btn for btn in create_airline if btn.is_displayed()]
    next(b for b in visible_buttons_create_airline if b.text == 'CREATE AIRLINE').click()
    screen.should_contain('Please fill in the company name.')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
        
    names = ['Company Name']
    texts = ['test airline name']
        
    # Input the data fields for creating the client
    complete_fields(screen, names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')

    # Ensure airline is created and the tab has been changed
    next(b for b in visible_buttons_create_airline if b.text == 'CREATE AIRLINE').click()
    screen.wait(1)
    screen.should_contain('Airline created with ID')
    
@pytest.mark.order(13)
def test_create_flight_booking(screen: Screen):
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
    
    # Flights tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    
    screen.find('Create Booking').click()
    screen.wait(6)
    
    create_booking = find_visible_buttons(screen)
    visible_buttons_create_booking = [btn for btn in create_booking if btn.is_displayed()]
    next(b for b in visible_buttons_create_booking if b.text == 'CREATE BOOKING').click()
    screen.should_contain('Please choose a client ID.')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable

    selects = screen.find_all_by_class('q-select')
    
    for s in selects:
        s.click()
        screen.wait(0.5)
        options = screen.find_all_by_class('q-item')
        options[0].click()
        screen.wait(0.5)

    # Ensure flight is created and the tab has been changes
    next(b for b in visible_buttons_create_booking if b.text == 'CREATE BOOKING').click()
    screen.wait(1)
    screen.should_contain('Flight booking created')
    
@pytest.mark.order(14)
def test_create_available_flight(screen: Screen):
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
    
    # Flights tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('Create Available Flight').click()
    screen.wait(6)

    selects = screen.find_all_by_class('q-select')
    
    for s in selects:
        s.click()
        screen.wait(0.5)
        options = screen.find_all_by_class('q-item')
        options[0].click()
        screen.wait(0.5)

    create_flight = find_visible_buttons(screen)
    visible_buttons_create_flight = [btn for btn in create_flight if btn.is_displayed()]
    next(b for b in visible_buttons_create_flight if b.text == 'CREATE FLIGHT').click()
    screen.should_not_contain('Available flight created')
    screen.should_contain('Please fill in all flight details')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    names = ['Start City', 'End City']
    texts = ['test start', 'test end']
        
    # Input the data fields for creating the client
    complete_fields(screen, names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')
    
    # Use default for the date fields

    # Ensure flight is created and the tab has been changed
    next(b for b in visible_buttons_create_flight if b.text == 'CREATE FLIGHT').click()
    screen.wait(0.5)
    screen.should_contain('Available flight created')
    