import pytest
from nicegui.testing import Screen
from app import startup
from tests.utils import find_visible_buttons, login_as_admin

@pytest.mark.order(10)
def test_tabs_after_login(screen: Screen):
    """
    End-to-end test to verify that all tabs and context-sensitive buttons are correctly displayed
    after logging in.

    The test performs the following:
        - Logs in as an admin
        - Navigates through each entity tab ('Clients', 'Airlines', etc.)
        - Verifies that all main tabs and action tabs are present
        - Verifies correct context-specific buttons appear in 'Create', 'View', 'Edit', and 'Delete' tabs

    Args:
        screen (Screen): The NiceGUI testing screen instance.
    """
    login_as_admin(screen)
    
    # Create a function checking for all tabs being visible
    def check_visible_tabs():
        """Asserts that all expected tabs are visible after login."""
        screen.should_contain('Clients')
        screen.should_contain('Airlines')
        screen.should_contain('Flights Bookings')
        screen.should_contain('Available Flights')
        screen.should_contain('Create')
        screen.should_contain('View')
        screen.should_contain('Edit')
        screen.should_contain('Delete')
    
    def create_tab_check(upper):
        """Checks button visibility in the 'Create' tab for the selected entity type."""
        screen.find('Create').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)
        
        if upper.capitalize() == 'Clients':
            assert any(b.text == 'CREATE CLIENT' for b in visible_buttons)
            assert not any(b.text in {'CREATE AIRLINE', 'CREATE BOOKING', 'CREATE FLIGHT',
                                      'SEARCH', 'EDIT', 'DELETE CLIENT'} for b in visible_buttons)

        elif upper.capitalize() == 'Airlines':
            assert any(b.text == 'CREATE AIRLINE' for b in visible_buttons)
            assert not any(b.text in {'CREATE CLIENT', 'CREATE BOOKING', 'CREATE FLIGHT',
                                      'SEARCH', 'EDIT', 'DELETE CLIENT'} for b in visible_buttons)

        elif upper.capitalize() == 'Flights Bookings':
            assert any(b.text == 'CREATE BOOKING' for b in visible_buttons)
            assert not any(b.text in {'CREATE CLIENT', 'CREATE AIRLINE', 'CREATE FLIGHT',
                                      'SEARCH', 'EDIT', 'DELETE CLIENT'} for b in visible_buttons)

        elif upper.capitalize() == 'Available Flights':
            assert any(b.text == 'CREATE FLIGHT' for b in visible_buttons)
            assert not any(b.text in {'CREATE CLIENT', 'CREATE AIRLINE', 'CREATE BOOKING',
                                      'SEARCH', 'EDIT', 'DELETE CLIENT'} for b in visible_buttons)
        
    def view_tab_check():
        """Checks visibility of the 'Search' button in the 'View' tab."""
        screen.find('View').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert any(b.text == 'SEARCH' for b in visible_buttons)
        assert not any(b.text in {'CREATE CLIENT', 'EDIT', 'DELETE CLIENT'} for b in visible_buttons)
        
    def edit_tab_check():
        """Checks visibility of the 'Edit' button in the 'Edit' tab."""
        screen.find('Edit').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert any(b.text == 'EDIT' for b in visible_buttons)
        assert not any(b.text in {'CREATE CLIENT', 'SEARCH', 'DELETE CLIENT'} for b in visible_buttons)
        
    def delete_tab_check(upper):
        """Checks delete button visibility for each entity type in the 'Delete' tab."""
        screen.find('Delete').click()
        screen.wait(1)
        check_visible_tabs()
        
        visible_buttons = find_visible_buttons(screen)

        assert not any(b.text in {'CREATE CLIENT', 'SEARCH', 'EDIT'} for b in visible_buttons)
        
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