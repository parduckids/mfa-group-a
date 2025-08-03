import pytest
from nicegui.testing import Screen
from app import startup
import platform
from tests.utils import find_visible_buttons, get_highest_id_value, input_text
from pathlib import Path

@pytest.mark.order(27)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    delete_button = find_visible_buttons(screen)
    visible_buttons_delete = [btn for btn in delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_delete if b.text == 'DELETE CLIENT').click()
    screen.wait(1)
    screen.should_contain('Client not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE CLIENT').click()
    screen.should_contain('Client not found')
    screen.wait(7) # wait for the notification to disappear
    
    clients_path = Path('src/data/clients.json')
    client_id = get_highest_id_value(clients_path, "ID")
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE CLIENT').click()
    screen.wait(0.5)
    screen.should_not_contain('Client not found')   
    screen.should_contain(f'Are you sure you want to delete client {client_id} and all their flights?')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE CLIENT').click()
    screen.wait(0.5)
    screen.should_contain(f'Are you sure you want to delete client {client_id} and all their flights?')
    
    yes_delete_button = find_visible_buttons(screen)
    visible_buttons_yes_delete = [btn for btn in yes_delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_yes_delete if b.text == 'YES, DELETE').click()
    screen.wait(1)
    screen.should_contain(f'Client {client_id} and all associated flights have been deleted')
    
@pytest.mark.order(28)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(0.5)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    delete_button = find_visible_buttons(screen)
    visible_buttons_delete = [btn for btn in delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_delete if b.text == 'DELETE AIRLINE').click()
    screen.wait(1)
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE AIRLINE').click()
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    airlines_path = Path('src/data/airlines.json')
    airlines_id = get_highest_id_value(airlines_path, 'ID')
    
    input_text(screen, airlines_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE AIRLINE').click()
    screen.wait(0.5)
    screen.should_not_contain('Client not found')   
    screen.should_contain(f'Are you sure you want to delete airline {airlines_id} and all associated flights?')

    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, airlines_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE AIRLINE').click()
    screen.wait(0.5)
    screen.should_contain(f'Are you sure you want to delete airline {airlines_id} and all associated flights?')
    
    yes_delete_button = find_visible_buttons(screen)
    visible_buttons_yes_delete = [btn for btn in yes_delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_yes_delete if b.text == 'YES, DELETE').click()
    screen.wait(1)
    screen.should_contain(f'Airline {airlines_id} and all associated flights have been deleted')
    
@pytest.mark.order(29)
def test_delete_flight_bookings(screen: Screen):
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
    
    buttons = screen.find_all_by_class('q-btn')
    buttons[-1].click()
    screen.wait(0.5)
    screen.should_contain(f'Are you sure you want to delete this flight?')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    screen.should_not_contain(f'Are you sure you want to delete this flight?')
    
    buttons[-1].click()
    screen.wait(0.5)
    yes_delete_button = find_visible_buttons(screen)
    visible_buttons_yes_delete = [btn for btn in yes_delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_yes_delete if b.text == 'YES, DELETE').click()
    screen.wait(0.5)
    screen.should_contain('Flight deleted successfully.')

@pytest.mark.order(30)
def test_delete_available_flights(screen: Screen):
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
    
    # Available flights tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('Delete').click()
    screen.wait(6)
    
    delete_button = find_visible_buttons(screen)
    visible_buttons_delete = [btn for btn in delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_delete if b.text == 'DELETE AVAILABLE FLIGHT').click()
    screen.wait(1)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE AVAILABLE FLIGHT').click()
    screen.wait(1)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    available_flights_path = Path('src/data/available_flights.json')
    available_flights_id = get_highest_id_value(available_flights_path, 'Flight_ID')
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE AVAILABLE FLIGHT').click()
    screen.wait(0.5)
    screen.should_not_contain('Client not found')   
    screen.should_contain(f'Are you sure you want to delete flight {available_flights_id}?')

    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_delete if b.text == 'DELETE AVAILABLE FLIGHT').click()
    screen.wait(0.5)
    screen.should_contain(f'Are you sure you want to delete flight {available_flights_id}?')
    
    yes_delete_button = find_visible_buttons(screen)
    visible_buttons_yes_delete = [btn for btn in yes_delete_button if btn.is_displayed()]
    next(b for b in visible_buttons_yes_delete if b.text == 'YES, DELETE').click()
    screen.wait(1)
    screen.should_contain(f'Flight {available_flights_id} has been deleted from available flights.')
    
