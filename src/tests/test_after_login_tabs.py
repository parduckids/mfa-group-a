import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons

@pytest.mark.order(10)
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
    login_button = find_visible_buttons(screen)
    visible_buttons_login = [btn for btn in login_button if btn.is_displayed()]
    next(b for b in visible_buttons_login if b.text == 'LOGIN').click()
    screen.wait(1)
    
    # Create a function checking for all tabs being visible
    def check_visible_tabs():
        # Assert all tabs exist
        screen.should_contain('Clients')
        screen.should_contain('Airlines')
        screen.should_contain('Flights Bookings')
        screen.should_contain('Available Flights')
        screen.should_contain('Create')
        screen.should_contain('View')
        screen.should_contain('Edit')
        screen.should_contain('Delete')
    
    def create_tab_check(upper):
        screen.find('Create').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)
        
        if upper.capitalize() == 'Clients':
            assert any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert not any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert not any(b.text == 'CREATE BOOKING' for b in visible_buttons), 'Create Booking button should not be visible'
            assert not any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
            
        elif upper.capitalize() == 'Airlines':
            assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert not any(b.text == 'CREATE BOOKING' for b in visible_buttons), 'Create Booking button should not be visible'
            assert not any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
            
        elif upper.capitalize() == 'Flights Bookings':
            assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert not any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert any(b.text == 'CREATE BOOKING' for b in visible_buttons), 'Create Booking button should not be visible'
            assert not any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
            
        elif upper.capitalize() == 'Available Flights':
            assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should be visible'
            assert not any(b.text == 'CREATE AIRLINE' for b in visible_buttons), 'Create Airline button should not be visible'
            assert not any(b.text == 'CREATE BOOKING' for b in visible_buttons), 'Create Booking button should not be visible'
            assert any(b.text == 'CREATE FLIGHT' for b in visible_buttons), 'Create Flight button should not be visible'
            assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
            assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
            assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def view_tab_check():
        screen.find('View').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should be visible'
        assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should not be visible'
        assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def edit_tab_check():
        screen.find('Edit').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
        assert any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should be visible'
        assert not any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should not be visible'
        
    def delete_tab_check(upper):
        screen.find('Delete').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert not any(b.text == 'CREATE CLIENT' for b in visible_buttons), 'Create Client button should not be visible'
        assert not any(b.text == 'SEARCH' for b in visible_buttons), 'Search button should not be visible'
        assert not any(b.text == 'EDIT' for b in visible_buttons), 'Edit button should be visible'
        
        if upper.capitalize() == 'Clients':
            assert any(b.text == 'DELETE CLIENT' for b in visible_buttons), 'Delete Client button should be visible'
            
        elif upper.capitalize() == 'Airlines':
            assert any(b.text == 'DELETE AIRLINE' for b in visible_buttons), 'Delete Client button should be visible'
            
        elif upper.capitalize() == 'FLIGHTS BOOKINGS':
            assert not any(b.text == 'DELETE BOOKING' for b in visible_buttons), 'Delete Client button should be visible'
            
        elif upper.capitalize() == 'Available Flights':
            assert any(b.text == 'DELETE AVAILABLE FLIGHT' for b in visible_buttons), 'Delete Client button should be visible'
        
    # Clients tabs
    screen.find('Clients').click()
    screen.wait(0.5)
        
    check_visible_tabs()
        
    create_tab_check(upper='Clients')

    view_tab_check()

    edit_tab_check()
    
    delete_tab_check(upper='Clients')
    
    # Airlines tabs
    screen.find('Airlines').click()
    screen.wait(0.5)
            
    check_visible_tabs()
        
    create_tab_check(upper='Airlines')

    view_tab_check()

    edit_tab_check()
    
    delete_tab_check(upper='Airlines')
    
    # Flight Bookings tabs
    screen.find('Flights Bookings').click()
    screen.wait(0.5)
        
    check_visible_tabs()
        
    create_tab_check(upper='Flights Bookings')

    view_tab_check()

    edit_tab_check()
    
    delete_tab_check(upper='Flights Bookings')
    
    # Available Flights tabs
    screen.find('Available Flights').click()
    screen.wait(0.5)
        
    check_visible_tabs()
        
    create_tab_check(upper='Available Flights')

    view_tab_check()

    edit_tab_check()
    
    delete_tab_check(upper='Available Flights')