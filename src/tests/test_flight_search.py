import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.keys import Keys
from tests.utils import find_visible_buttons, mod, get_lowest_id_value
from pathlib import Path

@pytest.mark.order(9)
def test_flight_search(screen: Screen) -> None:
    screen.open('/')
    
    # Expand the panel
    screen.find('Flight Search ✈️').click()
    screen.wait(0.5)
    
    # Search button
    search_button = find_visible_buttons(screen)
    visible_buttons_search = [btn for btn in search_button if btn.is_displayed()]
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    
    screen.should_contain('No matching flights found. Please check the details and try again.')

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[2].send_keys('wrong')  
    inputs[3].send_keys('wrong')  
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_contain('No matching flights found. Please check the details and try again.')
    
    # Clear input
    inputs[2].click()
    inputs[2].send_keys(mod + 'a')
    inputs[2].send_keys(Keys.DELETE)
    inputs[3].click()
    inputs[3].send_keys(mod + 'a')
    inputs[3].send_keys(Keys.DELETE)
    
    clients_path = Path(__file__).resolve().parent.parent / 'data' / 'clients.json'
    airlines_path = Path(__file__).resolve().parent.parent / 'data' / 'airlines.json'
    client_id = get_lowest_id_value(clients_path, 'ID')
    airline_id = get_lowest_id_value(airlines_path, 'ID')

    inputs[2].send_keys(client_id)  
    inputs[3].send_keys(airline_id)  
    next(b for b in visible_buttons_search if b.text == 'SEARCH').click()
    screen.wait(0.5)
    screen.should_not_contain('No matching flights found. Please check the details and try again.')
    screen.should_contain(' matching flight(s):')
