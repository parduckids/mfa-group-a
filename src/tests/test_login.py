import pytest
from nicegui.testing import Screen
from app import startup
from selenium.webdriver.common.keys import Keys
from tests.utils import find_visible_buttons, mod

@pytest.mark.order(7)
def test_login_logoff(screen: Screen) -> None:
    screen.open('/')
    
    # Expand the panel first
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Click Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(1)
    screen.find('login successful')

    # Try to logout and confirm
    buttons_logout = find_visible_buttons(screen)
    visible_buttons_logout = [btn for btn in buttons_logout if btn.is_displayed()]
    next(b for b in visible_buttons_logout if b.text == 'LOGOUT').click()
    screen.wait(1)
    
    screen.find('Login')
    screen.find('logged out')

@pytest.mark.order(8)
def test_wrong_password(screen: Screen) -> None:
    screen.open('/')
    
    # Expand the panel first
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Confirm failed login with correct username and wrong password    
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('wrong')

    # Click Login
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(1)
    screen.find('invalid credentials')
    screen.should_contain('Username')
    screen.should_contain('Password')
    screen.wait(6) # Wait for the notification to dissappear
    
    # Confirm failed login with wrong username and wrong password
    inputs[0].click()
    inputs[0].send_keys(mod + 'a')
    inputs[0].send_keys(Keys.DELETE)
    inputs[1].click()
    inputs[1].send_keys(mod + 'a')
    inputs[1].send_keys(Keys.DELETE)

    inputs[0].send_keys('wrong')  
    inputs[1].send_keys('wrong')

    # Click Login
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(1)
    screen.find('invalid credentials')
    screen.should_contain('Username')
    screen.should_contain('Password')
    screen.wait(6) # Wait for the notification to dissappear

    # Confirm failed login with wrong username and correct password
    inputs[0].click()
    inputs[0].send_keys(mod + 'a')
    inputs[0].send_keys(Keys.DELETE) 
    inputs[1].click()
    inputs[1].send_keys(mod + 'a')
    inputs[1].send_keys(Keys.DELETE)
    
    inputs[0].send_keys('wrong')
    inputs[1].send_keys('admin') 

    # Click Login
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(1)
    screen.find('invalid credentials')
    screen.should_contain('Username')
    screen.should_contain('Password')