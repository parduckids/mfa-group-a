import pytest
from nicegui.testing import Screen
import json
from pathlib import Path
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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