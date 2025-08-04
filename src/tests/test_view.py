import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons, get_highest_id_value, input_text, login_as_admin
from pathlib import Path

@pytest.mark.order(15)
def test_view_client(screen: Screen):
    """
    End-to-end test for viewing client data.

    This test verifies that:
        - Admin can log in and navigate to the Clients > View section
        - Sample client data is correctly displayed on the page

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    """
    End-to-end test for viewing airline data.

    This test verifies that:
        - Admin can log in and navigate to the Airlines > View section
        - Sample airline data is correctly displayed on the page

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    """
    End-to-end test for viewing flight bookings.

    This test verifies that:
        - Admin can log in and navigate to Flights Bookings > View Bookings
        - Booking-related fields are present
        - Data is displayed and not empty

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    """
    End-to-end test for viewing available flights.

    This test verifies that:
        - Admin can log in and navigate to Available Flights > View Available Flight
        - Route-related flight data is displayed and visible

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
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
    """
    End-to-end test for client search functionality in the View tab.

    This test verifies that:
        - Searching with an invalid client ID displays no results
        - Searching with a valid client ID displays the expected result

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Clients tab
    screen.find('Clients').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    clients_path = Path(__file__).resolve().parent.parent / 'data' / 'clients.json'
    client_id = get_highest_id_value(clients_path, 'ID')
    
    input_text(screen, client_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   
    
@pytest.mark.order(20)
def test_view_airline_search(screen: Screen):
    """
    End-to-end test for airline search functionality in the View tab.

    This test verifies that:
        - Searching with an invalid airline ID displays no results
        - Searching with a valid airline ID displays the expected result

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Airlines tab
    screen.find('Airlines').click()
    screen.wait(0.5)
    
    screen.find('View').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    airlines_path = Path(__file__).resolve().parent.parent / 'data' / 'airlines.json'
    airline_id = get_highest_id_value(airlines_path, 'ID')
    
    input_text(screen, airline_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   
 
@pytest.mark.order(21)
def test_view_flight_bookings_search(screen: Screen):
    """
    End-to-end test for flight bookings search functionality in the View tab.

    This test verifies that:
        - Searching with an invalid client ID displays no results
        - Searching with a valid client ID displays the expected result

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights bookings tab
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
    
    screen.find('View Bookings').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable 
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    flights_bookings_path = Path(__file__).resolve().parent.parent / 'data' / 'flights.json'
    flights_booking_id = get_highest_id_value(flights_bookings_path, 'Client_ID')
    
    input_text(screen, 1)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   

@pytest.mark.order(22)
def test_view_available_flights_search(screen: Screen):
    """
    End-to-end test for available flights search functionality in the View tab.

    This test verifies that:
        - Searching with an invalid flight ID displays no results
        - Searching with a valid flight ID displays the expected result

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Flights bookings tab
    screen.find('Available Flights').click()
    screen.wait(0.5)
    
    screen.find('View Available Flight').click()
    screen.wait(0.5)
    
    input_text(screen, text='wrong')
    screen.wait(6) # Wait for the notification to disappear so the button is clickable
    
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No data available')
    
    available_flights_path = Path(__file__).resolve().parent.parent / 'data' / 'available_flights.json'
    available_flights_id = get_highest_id_value(available_flights_path, 'Flight_ID')
    
    input_text(screen, available_flights_id)
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No data available')   