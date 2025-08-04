import pytest
from nicegui.testing import Screen
import json
from pathlib import Path
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import Literal

# Use CMD on macOS, CTRL elsewhere for keyboard shortcuts
mod = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

def find_visible_buttons(screen):
    """
    Finds all visible button elements on the current screen.

    Args:
        screen (Screen): The NiceGUI testing screen instance.

    Returns:
        list: A list of visible button elements.
    """
    buttons = screen.find_all_by_tag('button')
    
    visible_buttons = [btn for btn in buttons if btn.is_displayed()]
    return visible_buttons

def get_highest_id_value(json_path: Path, key: str) -> int:
    """
    Get the highest integer value for a given key in a list of JSON objects.

    Args:
        json_path (Path): Path to the JSON file.
        key (str): Key to extract numeric values from.

    Returns:
        int: The highest integer value found for the given key. Returns 0 if none found.
    """
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return max((int(item[key]) for item in data if key in item), default=0)

def get_lowest_id_value(json_path: Path, key: str) -> int:
    """
    Get the lowest integer value for a given key in a list of JSON objects.

    Args:
        json_path (Path): Path to the JSON file.
        key (str): Key to extract numeric values from.

    Returns:
        int: The lowest integer value found for the given key. Returns 0 if none found.
    """
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return min((int(item[key]) for item in data if key in item), default=0)

def input_text(screen, text):
    """
    Inputs text into the last input field found on the screen.

    Selects the field, clears existing text, and types the new text.

    Args:
        screen (Screen): The NiceGUI testing screen instance.
        text (str): The text to input.
    """
    inputs = screen.find_all_by_tag('input')
    
    # Select the field and clear the content
    inputs[-1].click()
    inputs[-1].send_keys(mod + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    
    # Add text
    inputs[-1].send_keys(text)
    
def complete_fields(screen, names, texts):
    """
    Fills input fields based on their aria-label attribute.

    Simulates typing by sending characters one-by-one, with a delay.

    Args:
        screen (Screen): The NiceGUI testing screen instance.
        names (Union[str, list[str]]): The aria-label(s) of the input fields.
        texts (Union[str, list[str]]): Corresponding text(s) to input into each field.
    """
    if isinstance(names, str):
        names = [names]
    if isinstance(texts, str):
        texts = [texts] * len(names)

    for name, text in zip(names, texts):
        input_element = screen.selenium.find_element(By.XPATH, f'//*[@aria-label="{name.title()}"]')
        for char in text:
            input_element.send_keys(char)
            screen.wait(0.1)
            
def login_as_admin(screen):
    """
    Logs into the application as an admin user.

    Navigates to the login panel, fills in default admin credentials,
    and submits the login form.

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    screen.open('/')
    screen.find('Agent Login').click()
    screen.wait(0.5)

    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')
    inputs[1].send_keys('admin')

    login_buttons = [btn for btn in screen.find_all_by_tag('button') if btn.is_displayed()]
    next(b for b in login_buttons if b.text == 'LOGIN').click()
    screen.wait(0.5)
        
def generate_test_data(file_path: Path, num_entries: int, template_type: Literal['clients', 'flights', 'airlines', 'available_flights']):
    """
    Generate a mock JSON file with test data for the specified template type.

    Args:
        file_path (Path): The path where the JSON file should be saved.
        num_entries (int): Number of entries to generate.
        template_type (str): One of 'clients', 'flights', 'airlines', or 'available_flights'.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = []

    for i in range(1, num_entries + 1):
        if template_type == 'clients':
            data.append({
                "ID": i,
                "Type": "Client",
                "Name": f"Test Name {i}",
                "Address Line 1": f"Test Address {i}",
                "Address Line 2": "",
                "Address Line 3": "",
                "City": "Test City",
                "State": "",
                "Zip Code": f"{10000 + i}",
                "Country": "Test Country",
                "Phone Number": f"123-456-{1000 + i}"
            })
        elif template_type == 'flights':
            data.append({
                "Booking_ID": i,
                "Client_ID": (i % 5) + 1,
                "Airline_ID": (i % 2) + 1,
                "Flight_ID": i,
                "Date": "2026-12-01T10:00",
                "Start City": f"City {i}",
                "End City": f"Destination {i}",
                "Type": "Flight"
            })
        elif template_type == 'airlines':
            data.append({
                "ID": i,
                "Type": "Airline",
                "Company Name": f"Airline {i}"
            })
        elif template_type == 'available_flights':
            data.append({
                "Flight_ID": i,
                "Airline_ID": (i % 2) + 1,
                "Date": "2026-12-01T10:00",
                "Start City": f"Start City {i}",
                "End City": f"End City {i}",
                "Type": "Flight"
            })
        else:
            raise ValueError(f"Unsupported template type: {template_type}")

    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@pytest.fixture(scope='function')
def test_json_file(request):
    """
    Pytest fixture to generate a temporary JSON file for a given data template.

    Accepts a tuple (size, template_type) and creates the corresponding JSON file.
    Cleans up the file after the test completes.

    Args:
        request (FixtureRequest): Contains the (size, template_type) tuple.

    Yields:
        Path: Path to the generated JSON file.
    """
    size, template_type = request.param
    file_path = Path(__file__).resolve().parent.parent / 'data' / f'{template_type}_test_{size}.json'

    generate_test_data(file_path, size, template_type)

    yield file_path

    if file_path.exists():
        file_path.unlink()