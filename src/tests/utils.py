import pytest
from nicegui.testing import Screen
import json
from pathlib import Path
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

mod = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

def find_visible_buttons(screen):
    buttons = screen.find_all_by_tag('button')
    
    visible_buttons = [btn for btn in buttons if btn.is_displayed()]
    return visible_buttons

def get_highest_id_value(json_path: Path, key: str) -> int:
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return max((int(item[key]) for item in data if key in item), default=0)

def get_lowest_id_value(json_path: Path, key: str) -> int:
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return min((int(item[key]) for item in data if key in item), default=0)

def input_text(screen, text):
    inputs = screen.find_all_by_tag('input')
    
    # Select the field and clear the content
    inputs[-1].click()
    inputs[-1].send_keys(mod + 'a')
    inputs[-1].send_keys(Keys.DELETE)
    
    # Add text
    inputs[-1].send_keys(text)
    
def complete_fields(screen, names, texts):
    if isinstance(names, str):
        names = [names]
    if isinstance(texts, str):
        texts = [texts] * len(names)

    for name, text in zip(names, texts):
        input_element = screen.selenium.find_element(By.XPATH, f'//*[@aria-label="{name.title()}"]')
        for char in text:
            input_element.send_keys(char)
            screen.wait(0.1)