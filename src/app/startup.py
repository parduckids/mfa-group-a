from datetime import datetime
from nicegui import ui

import json
from pathlib import Path

# Paths for data files
data_dir = Path(__file__).parent.parent / 'data'
client_file = data_dir / 'clients.json'
airline_file = data_dir / 'airlines.json'
flight_file = data_dir / 'flights.json'
available_flight_file = data_dir / 'available_flights.json'


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
available_flights = load_json(available_flight_file)

def build_agent_view():
    """Builds the main agent view with tabs for managing clients, airlines, and flights."""
    # Define client fields
    client_fields = [
        'ID', 'Type', 'Name', 'Address Line 1', 'Address Line 2',
        'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
        'Phone Number'
    ]

    # Define which client fields are required for validation
    required_client_fields = [
        'Name', 'Address Line 1', 'City', 'Zip Code', 'Country', 'Phone Number'
    ]

    # Define airline fields
    airline_fields = ['ID', 'Type', 'Company Name']

    # Define flight fields
    flight_manage_columns = [
        {'name': 'Booking ID', 'label': 'Booking ID', 'field': 'Booking ID'},
        {'name': 'Flight ID', 'label': 'Flight ID', 'field': 'Flight ID'},
        {'name': 'Client ID', 'label': 'Client ID', 'field': 'Client ID'},
        {'name': 'Client', 'label': 'Client Name', 'field': 'Client'},
        {'name': 'Airline ID', 'label': 'Airline ID', 'field': 'Airline ID'},
        {'name': 'Airline', 'label': 'Airline Name', 'field': 'Airline'},
        {'name': 'Date', 'label': 'Date', 'field': 'Date'},
        {'name': 'Start City', 'label': 'Start City', 'field': 'Start City'},
        {'name': 'End City', 'label': 'End City', 'field': 'End City'}
    ]

    #Define available flight fields
    available_flight_fields = [
        'Flight_ID','Airline_ID', 'Date', 'Start City', 'End City'
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

        Returns the next airline ID by finding the maximum existing ID and adding 1.
        If no clients exist, returns 1.

        Returns:
            int: The next available airline ID.
        """
        if airlines:
            return max(int(a.get('ID', 0)) for a in airlines) + 1
        return 1

    def get_next_available_flight_id():
        """
        Generate the next available flight ID.

        Returns the next available flight ID by finding the maximum existing ID and adding 1.
        If no clients exist, returns 1.

        Returns:
            int: The next available flight ID.
        """
        if available_flights:
            return max(int(f.get('Flight_ID', 0)) for f in available_flights) + 1
        return 1

    def get_next_booking_id():
        """
        Generate the next available Booking ID.

        Returns the next available Booking ID by finding the maximum existing ID and adding 1.
        If no clients exist, returns 1.

        Returns:
            int: The next available flight ID.
        """
        if flights:
            return max(int(f.get('Booking_ID', 0)) for f in flights) + 1
        return 1


    def create_client():
        """
        Create a new client record and save it to the client file.

        This function:
        - Validates that all required fields are filled.
        - Generates a new unique client ID.
        - Collects input values into a record.
        - Sets the 'ID' and 'Type' fields.
        - Appends the new client to the clients list.
        - Persists the data to the Client JSON file.
        - Notifies the user of success.
        - Clears the input fields.
        - Switches to the 'View' tab.

        Returns:
            None
        """
        # Validate all required fields before proceeding
        validation_ok = all(inputs[field].validate() for field in required_client_fields)
        if not validation_ok:
            ui.notify('Please fill in all required fields.', type='warning')
            return

        new_id = get_next_client_id()
        record = {key: inp.value for key, inp in inputs.items()}
        record['ID'] = new_id
        record['Type'] = 'Client'

        clients.append(record)
        save_json(client_file, clients)

        # Update the client dropdown's options.
        new_client_options = {c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in clients}
        client_select.set_options(new_client_options)
        flight_delete_client_select.set_options(new_client_options)

        ui.notify(f'Client created with ID {new_id:09d}')

        for inp in inputs.values():
            inp.value = ''
        load_clients()
        # Switch to the view tab after creation
        client_ops.set_value(tab_client_manage)

    def create_airline():
        """
        Create a new airline record and save it to the airline file.

        This function:
        - Validates the company name field.
        - Generates a new unique airline ID.
        - Builds a record using the input company name.
        - Sets the 'ID', 'Type' and 'Company Name' fields.
        - Appends the new airline to the airlines list.
        - Persists the data to the Airline JSON file.
        - Notifies the user of success.
        - Clears the input field.
        - Switches to the 'View' tab.

        Returns:
            None
        """

        if not airline_input.validate():
            ui.notify('Please fill in the company name.', type='warning')
            return

        new_id = get_next_airline_id()
        record = {
            'ID': new_id,
            'Type': 'Airline',
            'Company Name': airline_input.value
        }

        airlines.append(record)
        save_json(airline_file, airlines)

        # Update the airline dropdown's options.
        new_airline_options = {a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a in airlines}
        airline_select.set_options(new_airline_options)

        ui.notify(f'Airline created with ID {new_id:09d}')

        airline_input.value = ''
        load_airlines()
        # Switch to the view tab after creation
        airline_ops.set_value(tab_airline_manage)

    flight_form_inputs = {}

    def create_flight():
        """
        Create a new flight record and save it to the flight file.

        This function:
        - Validates that all flight detail fields are filled.
        - Collects flight details from user input fields.
        - Builds a flight record with client, airline, date, and cities.
        - Adds the 'Client_ID', 'Airline_ID', 'Date', 'Start City', 'End City' and 'Type' fields.
        - Appends the record to the flights list.
        - Saves the updated list to a JSON file.
        - Notifies the user of success.
        - Clears the input fields.
        - Switches to the 'View' tab.

        Returns:
            None
        """

        flight_inputs = [
            client_select,
            flight_select,
            flight_form_inputs.get('airline_select'),
            flight_form_inputs.get('date_input'),
            flight_form_inputs.get('start_city'),
            flight_form_inputs.get('end_city')
        ]

        if not client_select.value:
            ui.notify('Please choose a client ID.', type='warning')
            return

        new_booking_id = get_next_booking_id

        record = {
            'Booking_ID': new_booking_id(),
            'Client_ID': client_select.value,
            'Airline_ID': flight_form_inputs['airline_select'].value,
            'Flight_ID': flight_select.value,
            'Date': flight_form_inputs['date_input'].value,
            'Start City': flight_form_inputs['start_city'].value,
            'End City': flight_form_inputs['end_city'].value,
            'Type': 'Flight'
        }

        flights.append(record)
        save_json(flight_file, flights)

        ui.notify('Flight booking created')

        for inp in flight_inputs:
            inp.value = ''

        # Reset date input to current time
        flight_form_inputs['date_input'].value = datetime.now().strftime('%Y-%m-%dT%H:%M')

        load_flights()
        flight_ops.set_value(tab_flight_manage)

    def create_available_flight():
        """
        Create a new available flight record and save it to the available flight file.

        This function:
        - Validates that all required flight fields are filled.
        - Generates a unique Flight_ID using get_next_available_Booking_ID().
        - Collects available flight details from user input fields.
        - Builds a available flight record with Flight_ID, Airline_ID, Date, Start City, and End City.
        - Appends the record to the available_flights list.
        - Saves the updated list to a JSON file.
        - Notifies the user of success.
        - Clears the input fields.
        - Switches to the 'View' tab.

        Returns:
            None
        """

        # Define which available flights fields are required for validation
        required_available_flights_fields = ['Airline_ID', 'Date', 'Start City', 'End City']

        inputs = {
            'Airline_ID': airline_select,
            'Date': date_input,
            'Start City': start_city_input,
            'End City': end_city_input
        }

        validation_ok = all(inputs[field].validate() for field in required_available_flights_fields)
        if not validation_ok:
            ui.notify('Please fill in all flight details.', type='warning')
            return

        # Generate a unique Flight_ID using helper function
        new_id = get_next_available_flight_id()

        record = {
            'Flight_ID': new_id,
            'Airline_ID': airline_select.value,
            'Date': date_input.value,
            'Start City': start_city_input.value,
            'End City': end_city_input.value
        }

        available_flights.append(record)
        save_json(available_flight_file, available_flights)

        ui.notify('Available flight created')

        for inp in inputs.values():
            inp.value = ''

        # Reset date input to current time
        date_input.value = datetime.now().strftime('%Y-%m-%dT%H:%M')

        load_available_flights()
        available_flight_ops.set_value(tab_available_flights)

    def load_clients():
        """
        Search for a client by ID and display the result in the clients table.
        When no id entered, show all clients.

        This function:
        - Retrieves and trims the client ID entered in the search input.
        - Filters the clients list for records matching the given ID.
        - Formats the ID to a 9-digit string for display.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = client_manage_search_id.value.strip()
        # If search query is empty, get all clients, otherwise filter by the query
        if not q:
            matched = [c.copy() for c in clients]
        else:
            matched = [c.copy() for c in clients if str(c.get('ID', '')).strip() == q]

        for r in matched:
            r['ID'] = f"{int(r['ID']):09d}"
        table_clients.rows = matched

    def load_airlines():
        """
        Search for an airline by ID and display the result in the airlines table.
        When no id entered, show all airlines.

        This function:
        - Retrieves and trims the airline ID entered in the search input.
        - Filters the airlines list for records matching the given ID.
        - Formats the ID to a 9-digit string for display.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = airline_manage_search_id.value.strip()
        # If search query is empty, get all airlines, otherwise filter by the query
        if not q:
            matched = [a.copy() for a in airlines]
        else:
            matched = [a.copy() for a in airlines if str(a.get('ID', '')).strip() == q]

        for r in matched:
            r['ID'] = f"{int(r['ID']):09d}"
        table_airlines.rows = matched

    def load_flights():
        """
        Search for flights by client ID and display the results in the flights table.
        When no id entered, show all flights.

        This function:
        - Retrieves and trims the client ID entered in the search input.
        - Filters the flights list for records matching the given client ID.
        - Resolves the corresponding client and airline names.
        - Constructs simplified flight records with client name, airline name, date, and cities.
        - Updates the table with the matching results.

        Returns:
            None
        """
        q = flight_booking_manage_search_id.value.strip()
        # If search query is empty, use all flights, otherwise filter by the query
        source_flights = flights if not q else [f for f in flights if str(f.get('Client_ID', '')).strip() == q]

        matched = []
        for f in source_flights:
            client_id = f.get('Client_ID')
            airline_id = f.get('Airline_ID')

            # Match using integers
            client = next((c for c in clients if c.get('ID') == client_id), {})
            airline = next((a for a in airlines if a.get('ID') == airline_id), {})

            record = {
                'Booking ID': f.get('Booking_ID', ""),
                'Flight ID': f.get('Flight_ID', ""),
                'Client ID': client_id,
                'Client': client.get('Name', ''),
                'Airline ID': airline_id,
                'Airline': airline.get('Company Name', ''),
                'Date': f.get('Date', ''),
                'Start City': f.get('Start City', ''),
                'End City': f.get('End City', '')
            }
            matched.append(record)

        table_flights.rows = matched

    def load_available_flights():
        """
        Search for flights by flight ID and display the results in the flights table.
        When no ID is entered, show all available flights.

        This function:
        - Retrieves and trims the flight ID entered in the search input.
        - Filters the available_flights list for records matching the given flight ID.
        - Resolves the corresponding airline name.
        - Constructs simplified flight records using the available_flight_fields list.
        - Updates the table with the matching results.

        Returns:
            None
        """
        available_flight_fields = ['Flight_ID', 'Airline_ID', 'Date', 'Start City', 'End City']
        q = flight_manage_search_id.value.strip()

        # If search query is empty, use all available flights, otherwise filter by Flight_ID
        source_flights = available_flights if not q else [
            f for f in available_flights if str(f.get('Flight_ID', '')).strip() == q
        ]

        matched = []
        for f in source_flights:
            airline = next((a for a in airlines if a['ID'] == f.get('Airline_ID')), {})
            record = {field: f.get(field, '') for field in available_flight_fields}
            record['Airline'] = airline.get('Company Name', '')
            matched.append(record)

        table_available_flights.rows = matched

    edit_inputs = {}
    edit_airline_inputs = {}
    edit_flight_inputs = {}
    edit_available_flights_inputs = {}

    def edit_clients():
        """
        Open a dialog to edit an existing client's information.

        Searches for a client by the ID entered in the search input field. If found,
        displays a dialog with input fields pre-filled with the client's data.
        The fields 'ID' and 'Type' are read-only; other fields can be edited.
        Upon saving, updates the client's data, saves the entire clients list to a JSON file,
        refreshes the UI client table, shows a success notification, and closes the dialog.

        If the client is not found, a warning notification is displayed.

        Returns:
            None
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

                Collects current values from the edit input fields, updates the client object,
                saves the full clients list to the JSON file, refreshes the client table in the UI,
                displays a success notification, and closes the edit dialog.

                Returns:
                    None
                """
                for field in client_fields:
                    client[field] = edit_inputs[field].value
                save_json(client_file, clients)
                load_clients()
                ui.notify('Client updated successfully', type='positive')
                dialog.close()

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                    'border border-black text-black bg-white'
                )
                ui.button('Save Changes', on_click=save_changes, color = 'green')
        dialog.open()

    def edit_airlines():
        """
        Open a dialog to edit an existing airline's information.

        Searches for an airline by ID entered in the search input field. If found,
        displays a dialog with the airline's current details pre-filled. The 'ID'
        and 'Type' fields are read-only. Users can edit other fields and either save
        the changes or cancel.

        If no matching airline is found, a warning notification is shown.

        Returns:
            None
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

                Retrieves updated values from input fields, modifies the corresponding airline record,
                saves the entire airlines list to the JSON file, refreshes the airline table in the UI,
                displays a success notification, and closes the dialog.

                Returns:
                    None
                """
                for field in airline_fields:
                    airline[field] = edit_airline_inputs[field].value
                save_json(airline_file, airlines)
                load_airlines()
                ui.notify('Airline updated successfully', type='positive')
                dialog.close()

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Save Changes', on_click=save_airline, color = 'green')
        dialog.open()

    def edit_flights():
        """
        Open a dialog to edit an existing flight's information.

        Searches for a flight using the `Booking ID` entered in the search input field.
        If a matching flight is found, displays a dialog with input fields pre-filled
        with the flight's current data. The user can edit the fields and save or cancel.

        If the flight is not found, displays a warning notification.

        Returns:
            None
        """
        q = flight_edit_search_id.value.strip()
        flight = next((f for f in flights if str(f.get('Booking_ID', '')).strip() == q), None)
        if not flight:
            ui.notify('Flight not found', type='warning')
            return
        edit_flight_inputs.clear()
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Edit Flight for Client ID: {flight.get('Client_ID')}").classes("text-lg font-bold mb-2")
            flight_fields = ['Client_ID', 'Airline_ID', 'Booking_ID', 'Date', 'Start City', 'End City']
            for field in flight_fields:
                value = flight.get(field, '')
                edit_flight_inputs[field] = ui.input(label=field, value=value).classes('mb-2 w-full')

            def save_flight():
                """
                Saves the modified flight data and updates the user interface.

                Collects updated values from input fields, validates and modifies the corresponding flight record,
                saves the updated flights list to a JSON file, refreshes the flight table in the UI,
                displays a success notification, and closes the dialog.

                Returns:
                    None
                """
                for field in flight_fields:
                    value = edit_flight_inputs[field].value
                    if 'ID' in field:
                        try:
                            flight[field] = int(value)
                        except ValueError:
                            ui.notify(f'{field} must be a number', type='warning')
                            return
                    else:
                        flight[field] = value

                #for field in flight_fields:
                #    flight[field] = edit_flight_inputs[field].value
                save_json(flight_file, flights)
                load_flights()
                ui.notify('Flight updated successfully', type='positive')
                dialog.close()

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Save Changes', on_click=save_flight, color = "green")
        dialog.open()

    def edit_available_flights():
        """
       Opens a dialog to edit an existing available flight's information.

       Searches for a flight using the Flight_ID entered in the search input field.
       If a matching flight is found, displays a dialog with input fields pre-filled
       with the flight's current data. The user can edit the fields and save the changes
       or cancel the operation.

       If no matching flight is found, displays a warning notification.

       Returns:
           None
       """
        #available_flight_fields = ['Flight_ID', 'Airline_ID', 'Date', 'Start City', 'End City']
        q = available_flight_edit_search_id.value.strip()

        flight = next((f for f in available_flights if str(f.get('Flight_ID', '')).strip() == q), None)
        if not flight:
            ui.notify('Flight not found', type='warning')
            return

        edit_available_flights_inputs.clear()
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Edit Flight ID: {flight.get('Flight_ID')}").classes("text-lg font-bold mb-2")
            #available_flight_fields = ['Flight_ID', 'Airline_ID', 'Date', 'Start City', 'End City']

            for field in available_flight_fields:
                value = flight.get(field, '')
                edit_available_flights_inputs[field] = ui.input(label=field, value=value).classes('mb-2 w-full')

            def save_available_flight():
                """
                Saves the modified flight data and updates the user interface.

                Collects updated values from input fields, validates and modifies the corresponding flight record,
                saves the updated flights list to a JSON file, refreshes the available flights table,
                shows a success notification, and closes the dialog.

                Returns:
                    None
                """
                for field in available_flight_fields:
                    value = edit_available_flights_inputs[field].value
                    if 'ID' in field:
                        try:
                            flight[field] = int(value)
                        except ValueError:
                            ui.notify(f'{field} must be a number', type='warning')
                            return
                    else:
                        flight[field] = value

                save_json(available_flight_file, available_flights)
                load_available_flights()
                ui.notify('Available Flight updated successfully', type='positive')
                dialog.close()

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                    'border border-black text-black bg-white'
                )
                ui.button('Save Changes', on_click=save_available_flight, color="green")
        dialog.open()

    def delete_client():
        """
        Initiates deletion of a client and all associated flights with user confirmation.

        Retrieves the client ID from the input field and searches for a matching client.
        If found, displays a confirmation dialog. Upon confirmation, the client is removed
        from the clients list, and all related flights are deleted. The updated data is saved,
        the UI is refreshed, and a success notification is shown.

        Returns:
            None
        """
        q = client_delete_search_id.value.strip()
        client_to_delete = next((c for c in clients if str(c.get('ID', '')).strip() == q), None)

        if not client_to_delete:
            ui.notify('Client not found', type='warning')
            return

        async def perform_delete():
            """
           Asynchronously deletes the selected client and all associated flights.

           Removes the client identified by `client_to_delete` from the clients list and
           deletes all flights linked to that client. Updates the stored JSON files, reloads
           client and flight data, refreshes related dropdown options, and clears the search input.
           Displays a success notification and closes the confirmation dialog.

           Returns:
               None
           """
            global clients, flights
            client_id_to_delete = client_to_delete['ID']
            clients = [c for c in clients if c['ID'] != client_id_to_delete]
            flights = [f for f in flights if f.get('Client_ID') != client_id_to_delete]

            save_json(client_file, clients)
            save_json(flight_file, flights)

            load_clients()
            load_flights()

            # Update the client dropdown's options.
            new_client_options = {c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in clients}
            client_select.set_options(new_client_options)
            flight_delete_client_select.set_options(new_client_options)

            ui.notify(f'Client {q} and all associated flights have been deleted.', type='positive')
            dialog.close()
            client_delete_search_id.value = ''

        with ui.dialog() as dialog, ui.card():
            ui.label(f"Are you sure you want to delete client {q} and all their flights?")
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Yes, delete', on_click=perform_delete, color='red-14')
        dialog.open()

    def delete_airline():
        """
        Initiates the deletion of an airline and its associated flights with user confirmation.

        Retrieves the airline ID from the input field and searches for a matching airline.
        If found, prompts the user with a confirmation dialog. Upon confirmation, the airline
        is removed from the airline list, and all related flights are also deleted. The updated
        data is saved, the UI is refreshed, and a success notification is shown.

        Returns:
            None
        """
        q = airline_delete_search_id.value.strip()
        airline_to_delete = next((a for a in airlines if str(a.get('ID', '')).strip() == q), None)

        if not airline_to_delete:
            ui.notify('Airline not found', type='warning')
            return

        async def perform_delete():
            """
            Asynchronously deletes the selected airline and all associated flights.

            Removes the selected airline from the airlines list and deletes all flights
            linked to that airline. Updates the stored JSON files, reloads airline and flight
            data, refreshes the airline dropdown options, and clears the input field. A success
            notification is displayed, and the confirmation dialog is closed.

            Returns:
                None
            """
            global airlines, flights
            airline_id_to_delete = airline_to_delete['ID']
            airlines = [a for a in airlines if a['ID'] != airline_id_to_delete]
            flights = [f for f in flights if f.get('Airline_ID') != airline_id_to_delete]

            save_json(airline_file, airlines)
            save_json(flight_file, flights)

            load_airlines()
            load_flights()

            # Update the airline dropdown's options.
            new_airline_options = {a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a in airlines}
            airline_select.set_options(new_airline_options)

            ui.notify(f'Airline {q} and all associated flights have been deleted.', type='positive')
            dialog.close()
            airline_delete_search_id.value = ''

        with ui.dialog() as dialog, ui.card():
            ui.label(f"Are you sure you want to delete airline {q} and all associated flights?")
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Yes, delete', on_click=perform_delete, color='red-14')
        dialog.open()

    def delete_available_flights():
        """
        Delete a flight from available_flights after confirmation.

        Searches for a flight by Flight_ID. If found, it presents a confirmation dialog.
        Upon confirmation, it removes the flight from the `available_flights` list,
        saves the updated list to the JSON file, and refreshes the UI.
        It does not delete all associated records as the flight may be removed but the same passenger with the same
        airline might be redirected onto a different flight
        """
        q = available_flight_delete_search_id.value.strip()

        flight_to_delete = next((f for f in available_flights if str(f.get('Flight_ID', '')).strip() == q), None)

        if not flight_to_delete:
            ui.notify('Flight not found', type='warning')
            return

        async def perform_delete():
            global available_flights
            available_flights = [f for f in available_flights if f.get('Flight_ID') != int(q)]

            save_json(available_flight_file, available_flights)
            load_available_flights()

            ui.notify(f'Flight {q} has been deleted from available flights.', type='positive')
            dialog.close()
            available_flight_delete_search_id.value = ''

        with ui.dialog() as dialog, ui.card():
            ui.label(f"Are you sure you want to delete flight {q}?")
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Yes, delete', on_click=perform_delete, color='red-14')
        dialog.open()

    def confirm_delete_single_flight(flight_to_delete):
        """
        Deletes a selected flight and updates the UI and data accordingly.

        Removes the specified flight from the flights list, saves the updated list to the JSON file,
        and refreshes both the main table and the deletable flights list. A success notification is shown,
        and the confirmation dialog is closed.

        Returns:
            None
        """

        async def perform_delete():
            """
            Asynchronously deletes the selected flight and updates the UI and data storage.

            Removes the specified flight from the in-memory flights list, saves the updated list
            to the JSON file, refreshes the main flight table and deletable flights list,
            and closes the confirmation dialog. A success notification is displayed.

            Returns:
                None
            """
            flights.remove(flight_to_delete)
            save_json(flight_file, flights)
            ui.notify('Flight deleted successfully.')
            # Refresh the main table and the dynamic list in the delete tab
            load_flights()
            update_deletable_flights_list(flight_to_delete['Client_ID'])
            dialog.close()

        with ui.dialog() as dialog, ui.card():
            airline = next((a for a in airlines if a['ID'] == flight_to_delete['Airline_ID']), {})
            ui.label(f"Are you sure you want to delete this flight?")
            ui.label(f"To: {flight_to_delete['End City']} on {flight_to_delete['Date']}")
            ui.label(f"Airline: {airline.get('Company Name', 'N/A')}")
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=dialog.close).classes(
                                'border border-black text-black bg-white'
                            )
                ui.button('Yes, delete', on_click=perform_delete, color='red-14')
        dialog.open()

    def update_deletable_flights_list(client_id):
        """
        Clear and repopulate the list of flights available for deletion for a given client.

        Args:
            client_id (int): The ID of the client whose flights should be listed.

        Returns:
            None
        """
        deletable_flights_container.clear()
        if not client_id:
            return

        client_flights = [f for f in flights if f.get('Client_ID') == client_id]

        with deletable_flights_container:
            if not client_flights:
                ui.label('No flights found for this client.')
                return

            ui.label(f'Flights for Client {client_id}:').classes('text-md font-bold mt-4')
            with ui.list().props('bordered separator'):
                for f in client_flights:
                    airline = next((a for a in airlines if a['ID'] == f['Airline_ID']), {})
                    with ui.item():
                        with ui.item_section():
                            ui.item_label(f"To: {f.get('End City', 'N/A')} on {f.get('Date', 'N/A')}")
                            ui.item_label(f"Airline: {airline.get('Company Name', 'N/A')}").props('caption')
                        with ui.item_section().props('side'):
                            # The f=f in lambda captures the current flight for the on_click event
                            ui.button(icon='delete', on_click=lambda f=f: confirm_delete_single_flight(f),
                                      color='red').props('flat dense')

    with ui.column().classes('w-full'):
        with ui.tabs().classes('w-full') as main_tabs:
            tab_clients = ui.tab('Clients')
            tab_airlines = ui.tab('Airlines')
            tab_flights_bookings = ui.tab('Flights Bookings')
            tab_available_flights = ui.tab('Available Flights')
        with ui.tab_panels(main_tabs, value=tab_clients).classes('w-full'):
            with ui.tab_panel(tab_clients):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Client Records').classes('text-xl')
                with ui.tabs().classes('w-full') as client_ops:
                    tab_client_create = ui.tab('Create Client')
                    tab_client_manage = ui.tab('View Client')
                    tab_client_edit = ui.tab('Edit Client')
                    tab_client_delete = ui.tab('Delete Client')
                with ui.tab_panels(client_ops).classes('w-full'):
                    with ui.tab_panel(tab_client_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            inputs = {}
                            for field in client_fields:
                                if field not in ['ID', 'Type']:
                                    inp = ui.input(label=field).classes('w-full mb-2')
                                    if field in required_client_fields:
                                        inp.validation = {
                                            'This field is required': lambda value: bool(value and value.strip())}
                                    inputs[field] = inp
                            ui.button('Create Client', on_click=create_client).classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_client_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_manage_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            table_clients = ui.table(
                                columns=[{'name': f, 'label': f, 'field': f} for f in client_fields], rows=[],
                                row_key='ID').classes('w-full mb-4')
                            ui.button('Search', on_click=load_clients).classes('w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                            load_clients()
                    with ui.tab_panel(tab_client_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_edit_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_clients).classes('w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_client_delete):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            client_delete_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            ui.button('Delete Client', on_click=delete_client).classes(
                                'w-full border border-red text-red bg-white'
                            )

            with ui.tab_panel(tab_airlines):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Airline Records').classes('text-xl')
                with ui.tabs().classes('w-full') as airline_ops:
                    tab_airline_create = ui.tab('Create Airline')
                    tab_airline_manage = ui.tab('View Airline')
                    tab_airline_edit = ui.tab('Edit Airline')
                    tab_airline_delete = ui.tab('Delete Airline')
                with ui.tab_panels(airline_ops).classes('w-full'):
                    with ui.tab_panel(tab_airline_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_input = ui.input(label='Company Name').classes('w-full mb-2')
                            airline_input.validation = {
                                'This field is required': lambda value: bool(value and value.strip())}
                            ui.button('Create Airline', on_click=create_airline).classes('mt-2 w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_airline_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_manage_search_id = ui.input(label='Airline ID').classes('w-full mb-2')
                            table_airlines = ui.table(
                                columns=[{'name': n, 'label': n, 'field': n} for n in airline_fields], rows=[],
                                row_key='ID').classes('w-full mb-4')
                            ui.button('Search', on_click=load_airlines).classes('w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                            load_airlines()
                    with ui.tab_panel(tab_airline_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_edit_search_id = ui.input(label='Airline ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_airlines).classes('w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_airline_delete):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_delete_search_id = ui.input(label='Airline ID').classes('w-full mb-2')
                            ui.button('Delete Airline', on_click=delete_airline).classes(
                                'w-full border border-red text-red bg-white'
                            )

            with ui.tab_panel(tab_flights_bookings):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Flight Records').classes('text-xl')
                with ui.tabs().classes('w-full') as flight_ops:
                    tab_flight_create = ui.tab('Create Booking')
                    tab_flight_manage = ui.tab('View Bookings')
                    tab_flight_edit = ui.tab('Edit Bookings')
                    tab_flight_delete = ui.tab('Delete Bookings')

                with ui.tab_panels(flight_ops).classes('w-full'):
                    with ui.tab_panel(tab_flight_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            # Container for dynamic flight form fields
                            flight_form_container = ui.column().classes('w-full')
                            flight_form_inputs = {}
                            def populate_flight_fields(e):
                                flight_form_container.clear()
                                with flight_form_container:
                                    # Create inputs and store in shared dictionary
                                    flight_form_inputs['airline_select'] = ui.select(
                                        {a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a in airlines},
                                        label='Airline'
                                    ).props('searchable true clearable').classes('w-full mb-2')
                                    flight_form_inputs['airline_select'].validation = {'This field is required': bool}

                                    flight_form_inputs['date_input'] = ui.input(label='Date').props(
                                        'type="datetime-local"').classes('w-full mb-2')

                                    flight_form_inputs['start_city'] = ui.input(label='Start City').classes(
                                        'w-full mb-2')
                                    flight_form_inputs['start_city'].validation = {
                                        'This field is required': lambda value: bool(value and value.strip())}

                                    flight_form_inputs['end_city'] = ui.input(label='End City').classes('w-full mb-2')
                                    flight_form_inputs['end_city'].validation = {
                                        'This field is required': lambda value: bool(value and value.strip())}

                                selected_id = str(e.value)

                                selected_flight = next(
                                    (f for f in available_flights if str(f['Flight_ID']) == selected_id), None
                                )

                                if selected_flight:
                                    flight_form_inputs['date_input'].set_value(selected_flight.get('Date', ''))
                                    flight_form_inputs['start_city'].set_value(selected_flight.get('Start City', ''))
                                    flight_form_inputs['end_city'].set_value(selected_flight.get('End City', ''))
                                    flight_form_inputs['airline_select'].value = selected_flight.get('Airline_ID', '')

                            # Initial UI elements
                            flight_select = ui.select(
                                {f['Flight_ID']: f"{f['Flight_ID']:09d}" for f in available_flights},
                                label='Select Flight', on_change=populate_flight_fields
                            ).props('clearable').classes('w-full mb-2')
                            flight_select.validation = {'This field is required': bool}

                            client_select = ui.select(
                                {c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in clients},
                                label='Client'
                            ).props('searchable true clearable').classes('w-full mb-2')
                            client_select.validation = {'This field is required': bool}

                            ui.button('Create Booking', on_click=create_flight).classes(
                                'mt-2 w-full w-full border border-black text-black bg-white'
                            )

                    with ui.tab_panel(tab_flight_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_booking_manage_search_id = ui.input(label='Client ID').classes('w-full mb-2')
                            table_flights = ui.table(columns=flight_manage_columns, rows=[], row_key='Client ID').classes(
                                'w-full mb-4')
                            ui.button('Search', on_click=load_flights).classes(
                                'w-full border border-black text-black bg-white'
                            )
                            load_flights()
                    with ui.tab_panel(tab_flight_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_edit_search_id = ui.input(label='Booking ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_flights).classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_flight_delete):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_delete_client_select = ui.select(
                                {c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in clients},
                                label='Select Client to see their flights',
                                on_change=lambda e: update_deletable_flights_list(e.value)
                            ).props('searchable true clearable').classes('w-full mb-2')
                            deletable_flights_container = ui.column().classes('w-full')

            with ui.tab_panel(tab_available_flights):
                with ui.row().classes('w-full justify-center mb-4'):
                    ui.label('Available Flights').classes('text-xl')
                with ui.tabs().classes('w-full') as available_flight_ops:
                    tab_available_flight_create = ui.tab('Create Available Flight')
                    tab_available_flight_manage = ui.tab('View Available Flight')
                    tab_available_flight_edit = ui.tab('Edit Available Flight')
                    tab_available_flight_delete = ui.tab('Delete Available Flight')
                with ui.tab_panels(available_flight_ops).classes('w-full'):
                    with ui.tab_panel(tab_available_flight_create):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            airline_select = ui.select(
                                {a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a in airlines},
                                label='Airline'
                            ).props('searchable true clearable').classes('w-full mb-2')
                            airline_select.validation = {'This field is required': bool}
                            default_date = datetime.now().strftime('%Y-%m-%dT%H:%M')

                            date_input = ui.input(label='Date', value=default_date).props(
                                'type="datetime-local"').classes('w-full mb-2')
                            date_input.validation = {'This field is required': bool}

                            start_city_input = ui.input(label='Start City').classes('w-full mb-2')
                            start_city_input.validation = {
                                'This field is required': lambda value: bool(value and value.strip())}

                            end_city_input = ui.input(label='End City').classes('w-full mb-2')
                            end_city_input.validation = {
                                'This field is required': lambda value: bool(value and value.strip())}

                            ui.button('Create Flight', on_click=create_available_flight).classes(
                                'mt-2 w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_available_flight_manage):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            flight_manage_search_id = ui.input(label='Flight ID').classes('w-full mb-2')
                            table_available_flights = ui.table(
                                columns=[{'name': n, 'label': n, 'field': n} for n in available_flight_fields], rows=[],
                                row_key='ID').classes('w-full mb-4')
                            ui.button('Search', on_click=load_available_flights).classes('w-full').classes(
                                'w-full border border-black text-black bg-white'
                            )
                            load_available_flights()
                    with ui.tab_panel(tab_available_flight_edit):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            available_flight_edit_search_id = ui.input(label='Flight ID').classes('w-full mb-2')
                            ui.button('Edit', on_click=edit_available_flights).classes(
                                'w-full border border-black text-black bg-white'
                            )
                    with ui.tab_panel(tab_available_flight_delete):
                        with ui.card().classes('mx-auto w-full p-4 shadow'):
                            available_flight_delete_search_id = ui.input(label='Flight ID').classes('w-full mb-2')
                            ui.button('Delete Available Flight', on_click=delete_available_flights).classes(
                                'w-full border border-red text-red bg-white'
                            )

def startup() -> None:
    """
    Initializes the application UI, including login and flight search interfaces.

    Sets up the initial state of the application with a split view.
    The left panel contains the agent login screen, while the right panel includes
    a flight search form. It also defines the agent dashboard, which is shown after
    a successful login. The UI elements are connected with internal logic for
    login validation, flight search, and logout behavior.

    Returns:
        None. The function modifies UI elements to build and display the application interface.
    """

    def perform_flight_search(client_input, airline_input, container, all_clients, all_airlines, all_flights):
        """
        Searches for flights matching the selected client and airline IDs, and displays results.

        Retrieves values from the client and airline input fields, filters the list of all flights to find matches,
        and displays a card for each found flight in the provided UI container. If no matching flights are found,
        an error card is shown.

        Args:
            client_input: UI input element containing the selected client ID.
            airline_input: UI input element containing the selected airline ID.
            container: UI container where results (flight cards) will be displayed.
            all_clients: List of all clients (each as a dictionary with keys like 'ID' and 'Name').
            all_airlines: List of all airlines (each as a dictionary with keys like 'ID' and 'Company Name').
            all_flights: List of all flights (each as a dictionary with keys like 'Client_ID', 'Airline_ID',
                         'Date', 'Start City', 'End City').

        Returns:
            None. Results are rendered directly in the provided container.
        """
        client_q = client_input.value
        airline_q = airline_input.value

        # Find ALL matching flights and store them in a list
        found_flights = [
            f for f in all_flights
            if str(f.get('Client_ID')) == str(client_q) and str(f.get('Airline_ID')) == str(airline_q)
        ]
        # Clear previous results
        container.clear()

        with container:
            if found_flights:
                ui.label(f'Found {len(found_flights)} matching flight(s):').classes('text-sm text-gray-600 mb-2')
                # Loop through each found flight and create a card for it
                for flight in found_flights:
                    client = next((c for c in all_clients if c['ID'] == flight['Client_ID']), {})
                    airline = next((a for a in all_airlines if a['ID'] == flight['Airline_ID']), {})

                    with ui.card().classes('w-full p-4 bg-gray-100 mb-4'):
                        ui.label(f'Your flight to {flight.get("End City", "your destination")}').classes(
                            'text-lg font-bold text-gray-700 mb-2')
                        with ui.column().classes('gap-1'):
                            ui.label(f'Client: {client.get("Name", "N/A")} ({flight.get("Client_ID")})')
                            ui.label(f'Airline: {airline.get("Company Name", "N/A")} ({flight.get("Airline_ID")})')
                            ui.label(f'Date: {flight.get("Date", "N/A")}')
                            ui.label(f'From: {flight.get("Start City", "N/A")}')
                            ui.label(f'To: {flight.get("End City", "N/A")}')
            else:
                # Error Card for when no flights are found
                with ui.card().classes('bg-red-50 border border-red-200 text-red-600 px-4 py-2 rounded-md shadow-sm'):
                    ui.label('⚠️ No matching flights found. Please check the details and try again.').classes('text-sm')

    agent_dashboard = None

    def handle_login(username_input, password_input):
        """
        Validates agent login credentials and updates the UI accordingly.

        If the provided username and password match the expected credentials,
        a success notification is shown, the welcome screen is hidden, and
        the agent dashboard is displayed. Otherwise, an error notification is shown.

        Args:
            username_input: UI input element containing the entered username.
            password_input: UI input element containing the entered password.

        Returns:
            None
        """
        if username_input.value == 'admin' and password_input.value == 'admin':
            ui.notify('login successful', type='positive')
            splitter.set_visibility(False)
            agent_dashboard.set_visibility(True)
        else:
            ui.notify('invalid credentials', type='negative')

    def logout():
        """
        Logs out the agent and returns to the welcome screen.

        This function hides the agent dashboard, makes the split view visible again,
        and displays a logout notification.

        Returns:
            None
        """
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
                    ui.button('Login', on_click=lambda: handle_login(username_input, password_input)).classes(
                        'border border-black text-black bg-white hover:bg-gray-100'
                    )
                    # Create a hidden marker for the bound level (before) so it can be captured by the test
                    ui.label().bind_text_from(splitter, 'value').classes('splitter-value-before hidden')

        with splitter.after:
            with ui.card().classes('w-full h-full').on('click', lambda: splitter.set_value(10)):
                with ui.column().classes('w-full items-center gap-4'):
                    ui.label('Flight Search ✈️').classes('text-2xl font-bold')
                    ui.label('Welcome! Please provide the flight details.')

                    client_id_input = ui.input('Client ID').props('outlined')
                    airline_id_input = ui.input('Airline ID').props('outlined')
                    results_container = ui.column().classes('w-full max-w-md mt-4')

                    ui.button('Search', on_click=lambda: perform_flight_search(
                        client_id_input,
                        airline_id_input,
                        results_container,
                        clients,
                        airlines,
                        flights
                    )).classes(
                    'border border-black text-black bg-white hover:bg-gray-100'
                   )
                    # Create a hidden marker for the bound level (after) so it can be captured by the test
                    ui.label().bind_text_from(splitter, 'value').classes('splitter-value-after hidden')

    with ui.card().classes('w-full h-screen hidden p-0') as agent_dashboard:
        agent_dashboard.set_visibility(False)
        with ui.column().classes('w-full items-center gap-4 p-6'):
            with ui.row(wrap=False).classes('w-full justify-between items-center'):
                ui.label('Agent Dashboard').classes('text-3xl font-bold')
                ui.button('Logout', on_click=logout).classes(
                    'border border-black text-black bg-white hover:bg-gray-100'
                )

            build_agent_view()
    # Create a hidden marker for the bound level so it can be captured by the test
    ui.label().bind_text_from(splitter, 'value').classes('splitter-value hidden')


# ui.run(title='Travel Agent Record Manager', reload=True)


# Render the full UI once the path is visited - used for testing
@ui.page('/')
def index():
    """Renders the full UI once the path is visited - used for testing."""
    startup()