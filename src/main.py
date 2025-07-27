import json
from pathlib import Path

# Paths for data files
data_dir = Path(__file__).parent / 'data'
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
    {'name': 'Client', 'label': 'Client', 'field': 'Client'},
    {'name': 'Airline', 'label': 'Airline', 'field': 'Airline'},
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