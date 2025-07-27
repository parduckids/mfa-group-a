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

# Generate next sequential ID for clients
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

# Generate next sequential ID for airlines
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

    for inp in [
        client_select,
        airline_select,
        date_input,
        start_city_input,
        end_city_input
    ]:
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
    q = search_id.value.strip()

    matched = [
        c.copy() for c in clients
        if str(c.get('ID', '')).strip() == q
    ]


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
    q = search_airline_id.value.strip()

    matched = [
        a.copy() for a in airlines
        if str(a.get('ID', '')).strip() == q
    ]

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
    q = search_flight_id.value.strip()
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

# ----- UI Structure (80% width centered) -----
with ui.column().classes('w-4/5 mx-auto'):

    # Main Tabs
    with ui.tabs().classes('w-full') as main_tabs:
        tab_clients = ui.tab('Clients')
        tab_airlines = ui.tab('Airlines')
        tab_flights = ui.tab('Flights')

    with ui.tab_panels(main_tabs).classes('w-full'):

        # ------- Client Records -------
        with ui.tab_panel(tab_clients):

            # Section title
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Client Records').classes('text-xl')

            # Client sub-tabs: Create and Manage
            with ui.tabs().classes('w-full') as client_ops:
                tab_client_create = ui.tab('Create')
                tab_client_manage = ui.tab('Manage')

            with ui.tab_panels(client_ops).classes('w-full'):

                # ---- Create Client ----
                with ui.tab_panel(tab_client_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Client').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        inputs = {}
                        for field in client_fields:
                            if field in ['ID', 'Type']:
                                continue
                            inputs[field] = ui.input(label=field).classes('w-full mb-2')

                        ui.button('Create Client', on_click = create_client).classes('mt-2 w-full')

                # ---- Manage Client ----
                with ui.tab_panel(tab_client_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_id = ui.input(label='Client ID').classes('w-full mb-2')

                        table_clients = ui.table(
                            columns=[
                                {'name': f, 'label': f, 'field': f} for f in client_fields
                            ],
                            rows=[],
                            row_key='ID',
                            pagination={'page_size': 5}
                        ).classes('w-full mb-4')

                        ui.button('Search', on_click = load_clients).classes('w-full')

        # ------- Airline Records -------
        with ui.tab_panel(tab_airlines):

            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Airline Records').classes('text-xl')

            # Airline sub-tabs: Create and Manage
            with ui.tabs().classes('w-full') as airline_ops:
                tab_airline_create = ui.tab('Create')
                tab_airline_manage = ui.tab('Manage')

            with ui.tab_panels(airline_ops).classes('w-full'):

                # ---- Create Airline ----
                with ui.tab_panel(tab_airline_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Airline').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        airline_input = ui.input(label='Company Name').classes('w-full mb-2')
                        ui.button('Create Airline', on_click = create_airline).classes('mt-2 w-full')

                # ---- Manage Airline ----
                with ui.tab_panel(tab_airline_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_airline_id = ui.input(label='Airline ID').classes('w-full mb-2')

                        table_airlines = ui.table(
                            columns=[
                                {'name': n, 'label': n, 'field': n} for n in airline_fields
                            ],
                            rows=[],
                            row_key='ID',
                            pagination={'page_size': 5}
                        ).classes('w-full mb-4')

                        ui.button('Search', on_click = load_airlines).classes('w-full')

        # ------- Flight Records -------
        with ui.tab_panel(tab_flights):

            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Flight Records').classes('text-xl')

            # Flight sub-tabs: Create and Manage
            with ui.tabs().classes('w-full') as flight_ops:
                tab_flight_create = ui.tab('Create')
                tab_flight_manage = ui.tab('Manage')

            with ui.tab_panels(flight_ops).classes('w-full'):

                # ---- Create Flight ----
                with ui.tab_panel(tab_flight_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Flight').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):

                        # Dropdown: Select client
                        client_select = ui.select(
                            label='Client',
                            options={
                                c['ID']: f"{c['Name']} {int(c['ID']):09d}"
                                for c in clients
                            }
                        ).props('searchable true clearable').classes('w-full mb-2')

                        # Dropdown: Select airline
                        airline_select = ui.select(
                            label='Airline',
                            options={
                                a['ID']: f"{a['Company Name']} {int(a['ID']):09d}"
                                for a in airlines
                            }
                        ).props('searchable true clearable').classes('w-full mb-2')

                        # Input fields
                        date_input = ui.input(label='Date').props('type="datetime-local"').classes('w-full mb-2')
                        start_city_input = ui.input(label='Start City').classes('w-full mb-2')
                        end_city_input = ui.input(label='End City').classes('w-full mb-2')

                        ui.button('Create Flight', on_click = create_flight).classes('mt-2 w-full')

                # ---- Manage Flight ----
                with ui.tab_panel(tab_flight_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')

                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_flight_id = ui.input(label='Client ID').classes('w-full mb-2')

                        table_flights = ui.table(
                            columns=flight_manage_columns,
                            rows=[],
                            row_key='Date',
                            pagination={'page_size': 5}
                        ).classes('w-full mb-4')

                        ui.button('Search', on_click = load_flights).classes('w-full')

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

ui.run(title = 'Travel Agent Record Manager', reload = True)
