from nicegui import ui
import json
from pathlib import Path

# Paths for data files
data_dir = Path(__file__).parent / 'data'
client_file = data_dir / 'clients.json'
airline_file = data_dir / 'airlines.json'
flight_file = data_dir / 'flights.json'

# Helpers to load & save JSON
def load_json(path, default=list):
    if not path.exists():
        return default()
    return json.loads(path.read_text())

def save_json(path, data):
    data_dir.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

# Initialize in-memory records
clients = load_json(client_file)
airlines = load_json(airline_file)
flights = load_json(flight_file)

# Generate next sequential ID for clients
def get_next_client_id():
    if clients:
        return max(int(c.get('ID', 0)) for c in clients) + 1
    return 1

# Generate next sequential ID for airlines
def get_next_airline_id():
    if airlines:
        return max(int(a.get('ID', 0)) for a in airlines) + 1
    return 1

# Define record fields
client_fields = [
    'ID', 'Type', 'Name', 'Address Line 1', 'Address Line 2',
    'Address Line 3', 'City', 'State', 'Zip Code', 'Country',
    'Phone Number'
]
airline_fields = ['ID', 'Type', 'Company Name']
flight_manage_columns = [
    {'name': 'Client', 'label': 'Client', 'field': 'Client'},
    {'name': 'Airline', 'label': 'Airline', 'field': 'Airline'},
    {'name': 'Date', 'label': 'Date', 'field': 'Date'},
    {'name': 'Start City', 'label': 'Start City', 'field': 'Start City'},
    {'name': 'End City', 'label': 'End City', 'field': 'End City'}
]

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
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Client Records').classes('text-xl')
            with ui.tabs().classes('w-full') as client_ops:
                tab_client_create = ui.tab('Create')
                tab_client_manage = ui.tab('Manage')
            with ui.tab_panels(client_ops).classes('w-full'):
                # Create Client
                with ui.tab_panel(tab_client_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Client').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        inputs = {}
                        for field in client_fields:
                            if field in ['ID', 'Type']:
                                continue
                            inputs[field] = ui.input(label=field).classes('w-full mb-2')
                        def create_client():
                            new_id = get_next_client_id()
                            record = {key: inp.value for key, inp in inputs.items()}
                            record['ID'] = new_id
                            record['Type'] = 'Client'
                            clients.append(record)
                            save_json(client_file, clients)
                            ui.notify(f'Client created with ID {new_id:09d}')
                            for inp in inputs.values():
                                inp.value = ''
                        ui.button('Create Client', on_click=create_client).classes('mt-2 w-full')

                # Manage Client
                with ui.tab_panel(tab_client_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_id = ui.input(label='Client ID').classes('w-full mb-2')
                        table_clients = ui.table(
                            columns=[{'name': f, 'label': f, 'field': f} for f in client_fields],
                            rows=[], row_key='ID', pagination={'page_size': 5}
                        ).classes('w-full mb-4')
                        def load_clients():
                            q = search_id.value.strip()
                            matched = [c.copy() for c in clients if str(c.get('ID','')).strip() == q]
                            for r in matched:
                                r['ID'] = f"{int(r['ID']):09d}"
                            table_clients.rows = matched
                        ui.button('Search', on_click=load_clients).classes('w-full')

        # ------- Airline Records -------
        with ui.tab_panel(tab_airlines):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Airline Records').classes('text-xl')
            with ui.tabs().classes('w-full') as airline_ops:
                tab_airline_create = ui.tab('Create')
                tab_airline_manage = ui.tab('Manage')
            with ui.tab_panels(airline_ops).classes('w-full'):
                # Create Airline
                with ui.tab_panel(tab_airline_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Airline').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        airline_input = ui.input(label='Company Name').classes('w-full mb-2')
                        def create_airline():
                            new_id = get_next_airline_id()
                            record = {'ID': new_id, 'Type': 'Airline', 'Company Name': airline_input.value}
                            airlines.append(record)
                            save_json(airline_file, airlines)
                            ui.notify(f'Airline created with ID {new_id:09d}')
                            airline_input.value = ''
                        ui.button('Create Airline', on_click=create_airline).classes('mt-2 w-full')

                # Manage Airline
                with ui.tab_panel(tab_airline_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_airline_id = ui.input(label='Airline ID').classes('w-full mb-2')
                        table_airlines = ui.table(
                            columns=[{'name': n, 'label': n, 'field': n} for n in airline_fields],
                            rows=[], row_key='ID', pagination={'page_size': 5}
                        ).classes('w-full mb-4')
                        def load_airlines():
                            q = search_airline_id.value.strip()
                            matched = [a.copy() for a in airlines if str(a.get('ID','')).strip() == q]
                            for r in matched:
                                r['ID'] = f"{int(r['ID']):09d}"
                            table_airlines.rows = matched
                        ui.button('Search', on_click=load_airlines).classes('w-full')

        # ------- Flight Records -------
        with ui.tab_panel(tab_flights):
            with ui.row().classes('w-full justify-center mb-4'):
                ui.label('Flight Records').classes('text-xl')
            with ui.tabs().classes('w-full') as flight_ops:
                tab_flight_create = ui.tab('Create')
                tab_flight_manage = ui.tab('Manage')
            with ui.tab_panels(flight_ops).classes('w-full'):
                # Create Flight
                with ui.tab_panel(tab_flight_create):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('New Flight').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        client_select = ui.select(
                            label='Client',
                            options={c['ID']: f"{c['Name']} {int(c['ID']):09d}" for c in clients}
                        ).props('searchable true clearable').classes('w-full mb-2')
                        airline_select = ui.select(
                            label='Airline',
                            options={a['ID']: f"{a['Company Name']} {int(a['ID']):09d}" for a in airlines}
                        ).props('searchable true clearable').classes('w-full mb-2')
                        date_input = ui.input(label='Date').props('type="datetime-local"').classes('w-full mb-2')
                        start_city_input = ui.input(label='Start City').classes('w-full mb-2')
                        end_city_input = ui.input(label='End City').classes('w-full mb-2')
                        def create_flight():
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
                        ui.button('Create Flight', on_click=create_flight).classes('mt-2 w-full')

                # Manage Flight: names
                with ui.tab_panel(tab_flight_manage):
                    with ui.row().classes('w-full justify-center mb-2'):
                        ui.label('Search / Update / Delete').classes('text-lg')
                    with ui.card().classes('mx-auto w-full p-4 shadow'):
                        search_flight_id = ui.input(label='Client ID').classes('w-full mb-2')
                        table_flights = ui.table(
                            columns=flight_manage_columns,
                            rows=[], row_key='Date', pagination={'page_size': 5}
                        ).classes('w-full mb-4')
                        def load_flights():
                            q = search_flight_id.value.strip()
                            matched = []
                            for f in flights:
                                if str(f.get('Client_ID','')).strip() == q:
                                    client = next((c for c in clients if c['ID']==f['Client_ID']), {})
                                    airline = next((a for a in airlines if a['ID']==f['Airline_ID']), {})
                                    record = {
                                        'Client': client.get('Name',''),
                                        'Airline': airline.get('Company Name',''),
                                        'Date': f.get('Date',''),
                                        'Start City': f.get('Start City',''),
                                        'End City': f.get('End City','')
                                    }
                                    matched.append(record)
                            table_flights.rows = matched
                        ui.button('Search', on_click=load_flights).classes('w-full')

# Run the application
ui.run(title='Travel Agent Record Manager', reload=True)