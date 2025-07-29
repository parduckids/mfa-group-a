import pytest
from nicegui.testing import User, Screen
from app import startup
from selenium.webdriver.common.keys import Keys
from pathlib import Path

pytest_plugins = ['nicegui.testing.plugin']

@pytest.mark.module_under_test(startup)
def test_tabs_after_login(screen: Screen):
    screen.open('/')
    
    # Expand the panel first
    screen.find('Agent Login').click()
    screen.wait(0.5)

    # Now fill in credentials
    inputs = screen.find_all_by_tag('input')
    inputs[0].send_keys('admin')  
    inputs[1].send_keys('admin')  

    # Click Login
    button = screen.find_all_by_tag('button')
    button[0].click()
    screen.wait(1)
    
    # Create a function checking for all tabs being visible
    def check_visible_tabs():
        # Assert all tabs exist
        screen.should_contain('Clients')
        screen.should_contain('Airlines')
        screen.should_contain('Flights')
        screen.should_contain('Create')
        screen.should_contain('View')
        screen.should_contain('Edit')
        screen.should_contain('Delete')
    
    def find_visible_buttons():
        buttons = screen.find_all_by_tag('button')
        
        visible_buttons = [btn for btn in buttons if btn.is_displayed()]
        return visible_buttons
    
    def create_tab_check(upper):
        screen.find('Create').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons()
        
        if upper.capitalize() == 'Clients':
            assert any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert not any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert not any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
            
        elif upper.capitalize() == 'Airlines':
            assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert not any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
            
        elif upper.capitalize() == 'Flights':
            assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert not any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def view_tab_check():
        screen.find('View').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons()

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should be visible'
        assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
        assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def edit_tab_check():
        screen.find('Edit').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons()

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
        assert any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should be visible'
        assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def delete_tab_check():
        screen.find('Delete').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons()

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
        assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should be visible'
        assert any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should be visible'
        
    # Clients tabs
    screen.find('Clients').click()
    screen.wait(0.5)
        
    check_visible_tabs()
        
    create_tab_check(upper='Clients')

    view_tab_check()

    edit_tab_check()
    
    # Airlines tabs
    screen.find('Airlines').click()
    screen.wait(0.5)
            
    check_visible_tabs()
        
    create_tab_check(upper='Airlines')

    view_tab_check()

    edit_tab_check()
    
    # Flights tabs
    screen.find('Flights').click()
    screen.wait(0.5)
        
    check_visible_tabs()
        
    create_tab_check(upper='Flights')

    view_tab_check()

    edit_tab_check()