import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons, complete_fields, login_as_admin

@pytest.mark.order(11)
def test_create_client(screen: Screen):
    """
    End-to-end test for creating a new client.

    This test verifies that:
        - Submitting the form with empty fields shows a validation error
        - Filling out the form correctly allows client creation
        - A success message is shown with the generated client ID

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Navigate to Clients > Create
    screen.find('Clients').click()
    screen.wait(0.5)
    screen.find('Create').click()
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
        
    # Attempt to submit empty form
    create_client = find_visible_buttons(screen)
    visible_buttons_create_client = [btn for btn in create_client if btn.is_displayed()]
    next(b for b in visible_buttons_create_client if b.text == 'CREATE CLIENT').click()
    screen.should_contain('Please fill in all required fields.')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
        
    # Fill in the required fields
    names = [
        'Name', 'Address Line 1', 'Address Line 2',
        'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
        'Phone Number'
    ]
    texts = [
        'test name', 'test address', '', '', 'test city', '',
        'test zip code', 'test country', 'test phone number'
    ]
    
    complete_fields(screen, names, texts)    
    screen.wait(0.5)
    screen.should_not_contain('This field is required')

    # Submit and verify
    next(b for b in visible_buttons_create_client if b.text == 'CREATE CLIENT').click()
    screen.wait(1)
    screen.should_contain('Client created with ID')
    
@pytest.mark.order(12)
def test_create_airline(screen: Screen):
    """
    End-to-end test for creating a new airline.

    This test verifies that:
        - Submitting without a company name triggers a validation error
        - Providing a valid name allows airline creation
        - A success message is shown with the generated airline ID

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    screen.find('Create').click()
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
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
    """
    End-to-end test for creating a new flight booking.

    This test verifies that:
        - Submitting with no client or flight selected shows a validation error
        - Selecting valid dropdown options allows booking creation
        - A success message confirms the booking was created

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    screen.find('Create Booking').click()
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
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
    """
    End-to-end test for creating a new available flight.

    This test verifies that:
        - Submitting with missing data shows a validation error
        - Completing required fields and selecting dropdowns allows creation
        - A success message confirms the flight was created

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('Create Available Flight').click()
    screen.wait(6) # Wait for the notification to disappear so the button is clickable

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
    