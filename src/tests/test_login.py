import pytest
from nicegui.testing import User, Screen
from app import startup

pytest_plugins = ['nicegui.testing.user_plugin']

@pytest.mark.module_under_test(startup)
async def test_login_logoff(user: User) -> None:
    await user.open('/')

    # Check whether you are on the login screen
    await user.should_see('Login')

    # Try to login with the correct password and confirm
    user.find('Username').type('admin')
    user.find('Password').type('admin').trigger('keydown.enter')
    await user.should_see('Logout')

    # Try to logout and confirm
    user.find('Logout').click()
    await user.should_see('Login')

@pytest.mark.module_under_test(startup)
async def test_wrong_password(user: User) -> None:
    await user.open('/')

    # Check whether you are on the login screen
    await user.should_see('Login')

    # Confirm failed login with correct username and wrong password
    user.find('Username').type('admin')
    user.find('Password').type('wrong').trigger('keydown.enter')
    await user.should_see('Username')
    await user.should_see('Password')

    # Confirm failed login with wrong username and wrong password
    user.find('Username').type('wrong')
    user.find('Password').type('wrong').trigger('keydown.enter')
    await user.should_see('Username')
    await user.should_see('Password')

    # Confirm failed login with wrong username and correct password
    user.find('Username').type('wrong')
    user.find('Password').type('admin').trigger('keydown.enter')
    await user.should_see('Username')
    await user.should_see('Password')