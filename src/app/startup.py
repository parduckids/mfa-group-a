from datetime import datetime
from nicegui import ui

import json
from pathlib import Path

# Paths for data files
data_dir = Path(__file__).parent.parent / 'data'
client_file = data_dir / 'clients.json'
airline_file = data_dir / 'airlines.json'
flight_file = data_dir / 'flights.json'


# Helpers to load & save JSON
def load_json(path, default=list):
    """
    Load JSON data from a file.

    If the specified path does not exist, return the result of the `default` callable instead.

    Args:
        path (Path): The path to the JSON file.
        default (Callable): A callable that returns a default value if the file does not exist.
                            Defaults to `list`.

    Returns:
        Any: The parsed JSON data, or the result of `default()` if the file is missing.
    """

    if not path.exists():
        return default()
    return json.loads(path.read_text())


def save_json(path, data):
    """
    Save data as a JSON file.

    Ensures that the directory for the given path exists before writing the data.

    Args:
        path (Path): The file path where the JSON data will be saved.
        data (Any): The data to be serialized and saved as JSON.

    Returns:
        None
    """
    data_dir.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


# Initialize in-memory records
clients = load_json(client_file)
airlines = load_json(airline_file)
flights = load_json(flight_file)


def build_agent_view():
    """Builds the main agent view with tabs for managing clients, airlines, and flights."""
    # Define client fields
    client_fields = [
        'ID', 'Type', 'Name', 'Address Line 1', 'Address Line 2',
        'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
        'Phone Number'
    ]

    # Define airline fields
    airline_fields = ['ID', 'Type', 'Company Name']

    # Define flight fields
    flight_manage_columns = [
        {'name': 'Client ID', 'label': 'Client ID', 'field': 'Client ID'},
        {'name': 'Client', 'label': 'Client Name', 'field': 'Client'},
        {'name': 'Airline ID', 'label': 'Airline ID', 'field': 'Airline ID'},
        {'name': 'Airline', 'label': 'Airline Name', 'field': 'Airline'},
        {'name': 'Date', 'label': 'Date', 'field': 'Date'},
        {'name': 'Start City', 'label': 'Start City', 'field': 'Start City'},
        {'name': 'End City', 'label': 'End City', 'field': 'End City'}
    ]

    def get_next_client_id():
        """
        Generate the next available client ID.

        Returns the next client ID by finding the maximum existing ID and adding 1.
        If no clients exist, returns 1.

        Returns:
            int: The next available client ID.
        """
        if clients:
            return max(int(c.get('ID', 0)) for c in clients) + 1
        return 1

    def get_next_airline_id():
        """
        Generate the next available airline ID.

        Returns the next client ID by finding the maximum existing ID and adding 1.
        If no clients exist, returns 1.

        Returns:
            int: The next available airline ID.
        """
        if airlines:
            return max(int(a.get('ID', 0)) for a in airlines) + 1
        return 1

    def create_client():
        """
        Create a new client record and save it to the client file.

        This function:
        - Generates a new unique client ID.
        - Collects input values into a record.
        - Sets the 'ID' and 'Type' fields.
        - Appends the new client to the clients list.
        - Persists the data to the Client JSON file.
        - Notifies the user of success.
        - Clears the input fields.

        Returns:
            None
        """
        new_id = get_next_client_id()
        record = {key: inp.value for key, inp in inputs.items()}
        record['ID'] = new_id
        record['Type'] = 'Client'

        clients.append(record)
        save_json(client_file, clients)

        ui.notify(f'Client created with ID {new_id:09d}')

        for inp in inputs.values():
            inp.value = ''

    def create_airline():
        """
        Create a new airline record and save it to the airline file.

        This function:
        - Generates a new unique airline ID.
        - Builds a record using the input company name.
        - Sets the 'ID', 'Type' and 'Company Name' fields.
        - Appends the new airline to the airlines list.
        - Persists the data to the Airline JSON file.
        - Notifies the user of success.
        - Clears the input field.

        Returns:
            None
        """
        new_id = get_next_airline_id()
        record = {
            'ID': new_id,
            'Type': 'Airline',
            'Company Name': airline_input.value
        }

        airlines.append(record)
        save_json(airline_file, airlines)

        ui.notify(f'Airline created with ID {new_id:09d}')

        airline_input.value = ''

    def create_flight():
        """
        Create a new flight record and save it to the flight file.

        This function:
        - Collects flight details from user input fields.
        - Builds a flight record with client, airline, date, and cities.
        - Adds the 'Client_ID', 'Airline_ID', 'Date', 'Start City', 'End City' and 'Type' fields.
        - Appends the record to the flights list.
        - Saves the updated list to a JSON file.
        - Notifies the user of success.
        - Clears the input fields.

        Returns:
            None
        """
        record = {
            'Client_ID': client_select.value,
            'Airline_ID': airline_select.value,
            'Date': date_input.value,
            'Start City': start_city_input.value,
            'End City': end_city_input.value,
            'Type': 'Flight'
        }

        flights.append(record)
        save_json(flight_file, flights)

        ui.notify('Flight created')

        for inp in [client_select, airline_select, date_input, start_city_input, end_city_input]:
            inp.value = ''

    def load_clients():
        """
        Search for a client by ID and display the result in the clients table.

        This function:
        - Retrieves and trims the client ID entered in the search input.
        - Filters the clients list for records matching the given ID.
        - Formats the ID to a 9-digit string for display.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = client_manage_search_id.value.strip()
        matched = [c.copy() for c in clients if str(c.get('ID', '')).strip() == q]
        for r in matched:
            r['ID'] = f"{int(r['ID']):09d}"
        table_clients.rows = matched

    def load_airlines():
        """
        Search for an airline by ID and display the result in the airlines table.

        This function:
        - Retrieves and trims the airline ID entered in the search input.
        - Filters the airlines list for records matching the given ID.
        - Formats the ID to a 9-digit string for display.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = airline_manage_search_id.value.strip()
        matched = [a.copy() for a in airlines if str(a.get('ID', '')).strip() == q]
        for r in matched:
            r['ID'] = f"{int(r['ID']):09d}"
        table_airlines.rows = matched

    def load_flights():
        """
        Search for flights by client ID and display the results in the flights table.

        This function:
        - Retrieves and trims the client ID entered in the search input.
        - Filters the flights list for records matching the given client ID.
        - Resolves the corresponding client and airline names.
        - Constructs simplified flight records with client name, airline name, date, and cities.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = flight_manage_search_id.value.strip()
        matched = []
        for f in flights:
            if str(f.get('Client_ID', '')).strip() == q:
                client = next((c for c in clients if c['ID'] == f['Client_ID']), {})
                airline = next((a for a in airlines if a['ID'] == f['Airline_ID']), {})
                record = {
                    'Client ID': f.get('Client_ID', ''),
                    'Client': client.get('Name', ''),
                    'Airline ID': f.get('Airline_ID', ''),
                    'Airline': airline.get('Company Name', ''),
                    'Date': f.get('Date', ''),
                    'Start City': f.get('Start City', ''),
                    'End City': f.get('End City', '')
                }
                matched.append(record)
        table_flights.rows = matched

    edit_inputs = {}
    edit_airline_inputs = {}
    edit_flight_inputs = {}

    def edit_clients():
        """
        Open a dialog to edit an existing client's information.

        This function searches for a client by the ID entered in the search input field.
        If a matching client is found, a dialog is displayed with input fields pre-filled with
        the client's data. The user can edit all fields except 'ID' and 'Type'. Upon saving,
        the client's data is updated and saved to a JSON file.

        The dialog includes options to save changes or cancel the operation.
        If the client ID is not found, a warning notification is shown.
        """
        q = client_edit_search_id.value.strip()
        client = next((c for c in clients if str(c.get('ID', '')).strip() == q), None)
        if not client:
            ui.notify('Client not found', type='warning')
            return
        edit_inputs.clear()
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Edit Client ID: {int(client['ID']):09d}").classes("text-lg font-bold mb-2")
            for field in client_fields:
                if field in ['ID', 'Type']:
                    edit_inputs[field] = ui.input(label=field, value=str(client.get(field, ''))).props(
                        'readonly').classes('mb-2 w-full')
                else:
                    edit_inputs[field] = ui.input(label=field, value=client.get(field, '')).classes('mb-2 w-full')

            def save_changes():
                """
                Save the modified client data and update the UI.

                This function collects the current values from the edit input fields,
                updates the client object, saves all clients to the JSON file, refreshes
                the UI table if visible, and displays a success notification. Finally, it
                closes the edit dialog.
                """
                for field in client_fields:
                    client[field] = edit_inputs[field].value
                save_json(client_file, clients)
                load_clients()
                ui.notify('Client updated successfully', type='positive')
                dialog.close()

            ui.button('Save Changes', on_click=save_changes).classes('mt-2 w-full')
            ui.button('Cancel', on_click=dialog.close).classes('mt-2 w-full')
        dialog.open()

    def edit_airlines():
        """
        Open a dialog to edit an existing airline's information.

        This function searches for an airline using the ID provided in the search
        input field. If the airline is found, a dialog is presented with the current details
        pre-filled. Fields 'ID' and 'Type' are shown as read-only. Users may edit the other
        fields and choose to either save the changes or cancel the operation.

        If no airline is found matching the entered ID, a warning notification is displayed.
        """
        q = airline_edit_search_id.value.strip()
        airline = next((a for a in airlines if str(a.get('ID', '')).strip() == q), None)
        if not airline:
            ui.notify('Airline not found', type='warning')
            return
        edit_airline_inputs.clear()
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Edit Airline ID: {int(airline['ID']):09d}").classes("text-lg font-bold mb-2")
            for field in airline_fields:
                if field in ['ID', 'Type']:
                    edit_airline_inputs[field] = ui.input(label=field, value=str(airline.get(field, ''))).props(
                        'readonly').classes('mb-2 w-full')
                else:
                    edit_airline_inputs[field] = ui.input(label=field, value=airline.get(field, '')).classes(
                        'mb-2 w-full')

            def save_airline():
                """
                Save the modified airline data and update the UI.

                This function retrieves values from the input fields, updates the corresponding
                airline record, writes all airline data back to the JSON file, refreshes the
                airline table in the UI, shows a success notification, and closes the dialog.
                """
                for field in airline_fields:
                    airline[field] = edit_airline_inputs[field].value
                save_json(airline_file, airlines)
                load_airlines()
                ui.notify('Airline updated successfully', type='positive')
                dialog.close()

            ui.button('Save Changes', on_click=save_airline).classes('mt-2 w-full')
            ui.button('Cancel', on_click=dialog.close).classes('mt-2 w-full')
        dialog.open()

    def edit_flights():
        """
        Open a dialog to edit an existing flight's information.

        This function searches for a flight using the `Client_ID` entered in the
        search input field. If a matching flight is found, a dialog
        is displayed containing input fields pre-filled with the flight's current data.
        The user may edit the fields and choose to save the changes or cancel the operation.

        If the flight is not found, a warning notification is displayed.
        """
        q = flight_edit_search_id.value.strip()
        flight = next((f for f in flights if str(f.get('Client_ID', '')).strip() == q), None)
        if not flight:
            ui.notify('Flight not found', type='warning')
            return
        edit_flight_inputs.clear()
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Edit Flight for Client ID: {flight.get('Client_ID')}").classes("text-lg font-bold mb-2")
            flight_fields = ['Client_ID', 'Airline_ID', 'Date', 'Start City', 'End City']
            for field in flight_fields:
                value = flight.get(field, '')
                edit_flight_inputs[field] = ui.input(label=field, value=value).classes('mb-2 w-full')

            def save_flight():
                """
                Save the modified flight data and update the UI.

                This function collects updated values from the input fields, modifies
                the corresponding flight record, saves the updated list to the JSON file,
                refreshes the UI flight table, displays a success notification, and closes
                the dialog.
                """
                for field in flight_fields:
                    flight[field] = edit_flight_inputs[field].value
                save_json(flight_file, flights)
                load_flights()
                ui.notify('Flight updated successfully', type='positive')
                dialog.close()

            ui.button('Save Changes', on_click=save_flight).classes('mt-2 w-full')
            ui.button('Cancel', on_click=dialog.close).classes('mt-2 w-full')
        dialog.open()

    with ui.column().classes('w-full'):
        with ui.tabs().classes('w-full') as main_tabs:
            tab_clients = ui.tab('Clients')
            tab_airlines = ui.tab('Airlines')
            tab_flights = ui.tab('Flights')
        with ui.tab_panels(main_tabs, value=tab_clients).classes('w-full'):
            with ui.tab_panel(tab_clients):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Client Records').classes('text-xl')
                with ui.tabs().classes('w-full') as client_ops:
                    tab_client_create = ui.tab('Create')
                    tab_client_manage = ui.tab('Manage')
                    tab_client_edit = ui.tab('Edit')
                with ui.tab_panels(client_ops).classes('w-full'):
                    with ui.tab_panel(tab_client_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            inputs = {}
                            for field in client_fields:
                                if field not in ['ID', 'Type']:
                                    inputs[field] = ui.input(label=field).classes('w-full mb-2')
                            ui.button('Create Client', on_click=create_client).classes('mt-2 w-full')
                    with ui.tab_panel(tab_client_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_manage_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            table_clients = ui.table(
                                columns=[{'name': f, 'label': f, 'field': f} for f in client_fields], rows=[],
                                row_key='ID').classes('w-full mb-4')
                            ui.button('Search', on_click=load_clients).classes('w-full')
                    with ui.tab_panel(tab_client_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_edit_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_clients).classes('w-full')
            with ui.tab_panel(tab_airlines):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Airline Records').classes('text-xl')
                with ui.tabs().classes('w-full') as airline_ops:
                    tab_airline_create = ui.tab('Create')
                    tab_airline_manage = ui.tab('Manage')
                    tab_airline_edit = ui.tab('Edit')
                with ui.tab_panels(airline_ops).classes('w-full'):
                    with ui.tab_panel(tab_airline_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_input = ui.input(label='Company Name').classes('w-full mb-2')
                            ui.button('Create Airline', on_click=create_airline).classes('mt-2 w-full')
                    with ui.tab_panel(tab_airline_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_manage_search_id = ui.input(label='Airline ID').classes('w-full mb-2')
                            table_airlines = ui.table(
                                columns=[{'name': n, 'label': n, 'field': n} for n in airline_fields], rows=[],
                                row_key='ID').classes('w-full mb-4')
                            ui.button('Search', on_click=load_airlines).classes('w-full')
                    with ui.tab_panel(tab_airline_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_edit_search_id = ui.input(label='Airline ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_airlines).classes('w-full')
            with ui.tab_panel(tab_flights):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Flight Records').classes('text-xl')
                with ui.tabs().classes('w-full') as flight_ops:
                    tab_flight_create = ui.tab('Create')
                    tab_flight_manage = ui.tab('Manage')
                    tab_flight_edit = ui.tab('Edit')
                with ui.tab_panels(flight_ops).classes('w-full'):
                    with ui.tab_panel(tab_flight_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_select = ui.select(label='Client',
                                                      options={c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in
                                                               clients}).props('searchable true clearable').classes(
                                'w-full mb-2')
                            airline_select = ui.select(label='Airline',
                                                       options={a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a
                                                                in airlines}).props(
                                'searchable true clearable').classes('w-full mb-2')
                            date_input = ui.input(label='Date').props('type="datetime-local"').classes('w-full mb-2')
                            start_city_input = ui.input(label='Start City').classes('w-full mb-2')
                            end_city_input = ui.input(label='End City').classes('w-full mb-2')
                            ui.button('Create Flight', on_click=create_flight).classes('mt-2 w-full')
                    with ui.tab_panel(tab_flight_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_manage_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            table_flights = ui.table(columns=flight_manage_columns, rows=[], row_key='Date').classes(
                                'w-full mb-4')
                            ui.button('Search', on_click=load_flights).classes('w-full')
                    with ui.tab_panel(tab_flight_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_edit_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_flights).classes('w-full')


def startup() -> None:
    """Initializes the application, setting up the login screen and the protected agent dashboard."""
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

    with ui.splitter(value=50).classes('w-full h-screen') as splitter:
        with splitter.before:
            with ui.card().classes('w-full h-full').on('click', lambda: splitter.set_value(90)):
                with ui.column().classes('w-full items-center gap-4'):
                    ui.label('Agent Login').classes('text-2xl font-bold')
                    username_input = ui.input('Username').props('outlined')
                    password_input = ui.input('Password', password=True, password_toggle_button=True).props('outlined')
                    ui.button('Login', on_click=lambda: handle_login(username_input, password_input))
        with splitter.after:
            # when card is clicked, it sets the splitter value to 10
            with ui.card().classes('w-full h-full flight-card').on('click', lambda: splitter.set_value(10)):
                with ui.column().classes('w-full items-center gap-4'):
                    ui.label('Flight Search ✈️').classes('text-2xl font-bold')
                    ui.label('Welcome! Please provide the flight details.')
                    ui.input('Client ID').props('outlined')
                    ui.input('Flight Number').props('outlined')
                    ui.button('Search')
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
                    with ui.row().classes('mt-4'):
                        with ui.card().classes(
                                'bg-red-50 border border-red-200 text-red-600 px-4 py-2 rounded-md shadow-sm'):
                            ui.label('⚠️ No matching flights found. Please check the details and try again.').classes(
                                'text-sm')

    # agent dashboard (only visible after successful login)
    with ui.card().classes('w-full h-screen hidden p-0 dashboard-card') as agent_dashboard:
        agent_dashboard.set_visibility(False)
        with ui.column().classes('w-full items-center gap-4 p-6'):
            with ui.row(wrap=False).classes('w-full justify-between items-center'):
                ui.label('Agent Dashboard').classes('text-3xl font-bold')
                ui.button('Logout', on_click=logout)

            build_agent_view()
    # Create marker for the bound level so it can be captured by the test 
    ui.label().bind_text_from(splitter, 'value').classes('splitter-value')


ui.run(title='Travel Agent Record Manager', reload=True)



# Render the full UI once the path is visited - used for testing
@ui.page('/')
def index():
    startup()