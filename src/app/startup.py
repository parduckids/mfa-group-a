from datetime import datetime
from nicegui import ui

def startup() -> None:
    # Login
    # store login state
    agent_logged_in = False

    # placeholders for dynamic elements
    agent_dashboard = None

    def handle_login(username_input, password_input):
        '''Checks the entered credentials and logs in the agent if valid
        hides the welcome screen and shows the agent dashboard on successful login.In case the credentials are invalid, shows an error notification.'''
        if username_input.value == 'admin' and password_input.value == 'admin':
            ui.notify('login successful', type='positive')
            splitter.set_visibility(False)
            agent_dashboard.set_visibility(True)
        else:
            ui.notify('invalid credentials', type='negative')

    def logout():
        '''Logs out the agent and returns to the welcome screen
        hides the agent dashboard and makes the split view visible again.'''
        agent_dashboard.set_visibility(False)
        splitter.set_visibility(True)
        ui.notify('logged out')

    # create a splitter that divides the screen, starts on 50/50
    with ui.splitter(value=50).classes('w-full h-screen') as splitter:

        # left panel: agent login
        with splitter.before:
            # when card is clicked, it sets the splitter value to 90, making this panel take 90% of the width
            with ui.card().classes('w-full h-full').on('click', lambda: splitter.set_value(90)):
                with ui.column().classes('w-full items-center gap-4'):
                    ui.label('Agent Login').classes('text-2xl font-bold')
                    username_input = ui.input('Username').props('outlined')
                    password_input = ui.input('Password', password=True, password_toggle_button=True).props('outlined')
                    ui.button('Login', on_click=lambda: handle_login(username_input, password_input))

        # right panel:flight search
        with splitter.after:
            # when card is clicked, it sets the splitter value to 10
            with ui.card().classes('w-full h-full').on('click', lambda: splitter.set_value(10)):
                with ui.column().classes('w-full items-center gap-4'):
                    ui.label('Flight Search ✈️').classes('text-2xl font-bold')
                    ui.label('Welcome! Please provide the flight details.')
                    ui.input('Client ID').props('outlined')
                    ui.input('Flight Number').props('outlined')
                    ui.button('Search')

                    # example flight card (this will be hidden unless there is an actual flight found after searching)
                    with ui.card().classes('w-full max-w-md mt-4 p-4 bg-gray-100'):
                        ui.label('Example flight (this could be called: "Your flight to {end_city}") ').classes(
                            'text-sm text-gray-500 mb-2')
                        with ui.column().classes('gap-1'):
                            ui.label('Client ID: 1234')
                            ui.label('Airline ID: 567')
                            ui.label('Flight ID: 8910')
                            ui.label(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
                            ui.label('Start City: London')
                            ui.label('End City: New York')

                    with ui.row().classes('m-3'):
                        ui.label('OR')
                    # no results message (when no matches are found, static for now)
                    with ui.row().classes('mt-4'):
                        with ui.card().classes(
                                'bg-red-50 border border-red-200 text-red-600 px-4 py-2 rounded-md shadow-sm'):
                            ui.label('⚠️ No matching flights found. Please check the details and try again.').classes(
                                'text-sm')

    # agent dashboard (only visible after successful login)
    with ui.card().classes('w-full h-screen items-center justify-center hidden') as agent_dashboard:
        agent_dashboard.set_visibility(False)
        with ui.column().classes('items-center gap-4 p-6'):
            ui.label('Agent Dashboard').classes('text-3xl font-bold')
            ui.label('this is the protected agent view after login')
            ui.button('Logout', on_click=logout)
