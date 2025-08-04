import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons, get_highest_id_value, input_text, login_as_admin
from pathlib import Path

@pytest.mark.order(27)
def test_delete_client(screen: Screen):
    """
    End-to-end test for deleting a client.

    This test verifies that:
        - Attempting to delete with no or invalid ID shows an error message
        - Entering a valid client ID shows a confirmation dialog
        - Canceling the dialog prevents deletion
        - Confirming the dialog deletes the client and associated flights
        - A success message is shown

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE CLIENT').click()
    screen.should_contain('Client not found')
    screen.wait(7) # Wait for the notification to disappear so the button is clickable
    
    clients_path = Path(__file__).resolve().parent.parent / 'data' / 'clients.json'
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
    """
    End-to-end test for deleting an airline.

    This test verifies that:
        - Attempting to delete with no or invalid ID shows an error message
        - Entering a valid airline ID shows a confirmation dialog
        - Canceling the dialog prevents deletion
        - Confirming the dialog deletes the airline and associated flights
        - A success message is shown

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE AIRLINE').click()
    screen.should_contain('Airline not found')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    airlines_path = Path(__file__).resolve().parent.parent / 'data' / 'airlines.json'
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
    """
    End-to-end test for deleting a booked flight.

    This test verifies that:
        - A booked flight can be selected and deleted via dropdown and button
        - A confirmation dialog is shown before deletion
        - Canceling the dialog prevents deletion
        - Confirming the dialog deletes the booking
        - A success message is shown

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)  
    
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
    """
    End-to-end test for deleting an available flight.

    This test verifies that:
        - Attempting to delete with no or invalid ID shows an error message
        - Entering a valid flight ID shows a confirmation dialog
        - Canceling the dialog prevents deletion
        - Confirming the dialog deletes the available flight
        - A success message is shown

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    input_text(screen, text='wrong')
    next(b for b in visible_buttons_delete if b.text == 'DELETE AVAILABLE FLIGHT').click()
    screen.wait(1)
    screen.should_contain('Flight not found')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    available_flights_path = Path(__file__).resolve().parent.parent / 'data' / 'available_flights.json'
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
    
