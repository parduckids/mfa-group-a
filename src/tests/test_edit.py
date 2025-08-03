import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.by import By
import platform
from tests.utils import find_visible_buttons, mod, input_text, get_highest_id_value, login_as_admin
from pathlib import Path

@pytest.mark.order(23)
def test_edit_client(screen: Screen):
    """
    End-to-end test for editing an existing client.

    This test verifies that:
        - Attempting to edit without or with an invalid ID shows an error message
        - Entering a valid client ID opens the edit form
        - Canceling the form does not make changes
        - Editing the name field and saving updates the client
        - A success message is displayed after saving

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('Edit').click()
    screen.wait(6)
    
    edit_button = find_visible_buttons(screen)
    visible_buttons_edit = [btn for btn in edit_button if btn.is_displayed()]
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Client not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Client not found')
    screen.wait(6) # wait for the notification to disappear
    
    clients_path = Path(__file__).resolve().parent.parent / 'data' / 'clients.json'
    client_id = get_highest_id_value(clients_path, 'ID')
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_not_contain('Client not found')
    screen.should_contain('Edit Client ID:')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    save_changes_button = find_visible_buttons(screen)
    visible_buttons_save_changes = [btn for btn in save_changes_button if btn.is_displayed()]
    next(b for b in visible_buttons_save_changes if b.text == 'SAVE CHANGES').click()
    screen.wait(1)
    screen.should_contain('Client updated successfully')
    
@pytest.mark.order(24)
def test_edit_airline(screen: Screen):
    """
    End-to-end test for editing an existing airline.

    This test verifies that:
        - Attempting to edit without or with an invalid ID shows an error message
        - Entering a valid airline ID opens the edit form
        - Canceling the form does not make changes
        - Editing the company name and saving updates the airline
        - A success message is displayed after saving

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('Edit').click()
    screen.wait(6)
    
    edit_button = find_visible_buttons(screen)
    visible_buttons_edit = [btn for btn in edit_button if btn.is_displayed()]
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Airline not found')
    screen.wait(6) # wait for the notification to disappear
    
    airlines_path = Path(__file__).resolve().parent.parent / 'data' / 'airlines.json'
    airline_id = get_highest_id_value(airlines_path, 'ID')
    
    input_text(screen, airline_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_not_contain('Airline not found')
    screen.should_contain('Edit Airline ID:')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, airline_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Company Name"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    save_changes_button = find_visible_buttons(screen)
    visible_buttons_save_changes = [btn for btn in save_changes_button if btn.is_displayed()]
    next(b for b in visible_buttons_save_changes if b.text == 'SAVE CHANGES').click()
    screen.wait(1)
    screen.should_contain('Airline updated successfully')
    
@pytest.mark.order(25)
def test_edit_flight_bookings(screen: Screen):
    """
    End-to-end test for editing an existing flight booking.

    This test verifies that:
        - Attempting to edit without or with an invalid ID shows an error message
        - Entering a valid booking ID opens the edit form
        - Canceling the form does not make changes
        - Editing the 'Start City' and saving updates the booking
        - A success message is displayed after saving

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    
    screen.find('Edit').click()
    screen.wait(6)
    
    edit_button = find_visible_buttons(screen)
    visible_buttons_edit = [btn for btn in edit_button if btn.is_displayed()]
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(1)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    flights_bookings_path = Path(__file__).resolve().parent.parent / 'data' / 'flights.json'
    flights_booking_id = get_highest_id_value(flights_bookings_path, 'Booking_ID')
    
    input_text(screen, flights_booking_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_not_contain('Flight not found')
    screen.should_contain('Edit Flight for Client ID:')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, flights_booking_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Start City"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    save_changes_button = find_visible_buttons(screen)
    visible_buttons_save_changes = [btn for btn in save_changes_button if btn.is_displayed()]
    next(b for b in visible_buttons_save_changes if b.text == 'SAVE CHANGES').click()
    screen.wait(1)
    screen.should_contain('Flight updated successfully')
    
@pytest.mark.order(26)
def test_edit_available_flights(screen: Screen):
    """
    End-to-end test for editing an existing available flight.

    This test verifies that:
        - Attempting to edit without or with an invalid ID shows an error message
        - Entering a valid available flight ID opens the edit form
        - Canceling the form does not make changes
        - Editing the 'Start City' and saving updates the flight
        - A success message is displayed after saving

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('Edit').click()
    screen.wait(6)
    
    edit_button = find_visible_buttons(screen)
    visible_buttons_edit = [btn for btn in edit_button if btn.is_displayed()]
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(1)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_contain('Flight not found')
    screen.wait(6) # wait for the notification to disappear
    
    available_flights_path = Path(__file__).resolve().parent.parent / 'data' / 'available_flights.json'
    available_flights_id = get_highest_id_value(available_flights_path, 'Flight_ID')
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    screen.should_not_contain('Flight not found')
    screen.should_contain('Edit Flight ID:')
    
    cancel_button = find_visible_buttons(screen)
    visible_buttons_cancel = [btn for btn in cancel_button if btn.is_displayed()]
    next(b for b in visible_buttons_cancel if b.text == 'CANCEL').click()
    screen.wait(1)
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_edit if b.text == 'EDIT').click()
    screen.wait(0.5)
    input_element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Start City"]')
    input_element.send_keys(' added text')
    screen.wait(0.5)
    
    save_changes_button = find_visible_buttons(screen)
    visible_buttons_save_changes = [btn for btn in save_changes_button if btn.is_displayed()]
    next(b for b in visible_buttons_save_changes if b.text == 'SAVE CHANGES').click()
    screen.wait(1)
    screen.should_contain('Flight updated successfully')
    