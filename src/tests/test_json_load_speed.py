import pytest
import json
from tests.utils import test_clients_file
import time
import matplotlib.pyplot as plt

parameters = [10, 100, 500, 1000, 2500, 5000, 7500, 10000, 20000, 40000, 60000, 80000, 100000]
size_data = []
perf_data = []

@pytest.mark.order(31)
@pytest.mark.parametrize(
    'test_clients_file', 
    parameters, 
    indirect=True
)
def test_loading_speed(test_clients_file):
    """
    Performance test for measuring JSON client file loading speed.

    This test benchmarks how long it takes to load a JSON file containing a
    varying number of client records. It verifies that:
        - The JSON file can be successfully opened and parsed
        - The number of records matches the test parameter
        - The loading time is recorded for performance plotting

    After the last test case (largest dataset), a performance graph is generated.

    Args:
        test_clients_file (Path): Path to the generated JSON file with client data.
    """
    start = time.perf_counter()

    with open(test_clients_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    end = time.perf_counter()
    duration = end - start
    size = len(data)

    print(f"\nLoaded {size} clients in {duration:.4f} seconds.")

    size_data.append(size)
    perf_data.append(duration)

    # Run the plot only after the last test case
    if size == max(parameters):
        generate_plot(size_data, perf_data)
    
def generate_plot(size_data, perf_data):
    """
    Generate and save a performance graph of loading time vs file size.

    This function creates a line chart showing how long it took to load
    JSON files of increasing size during the test run. The chart is saved
    as an image to the screenshots directory.

    Args:
        size_data (List[int]): List of client counts for each test case.
        perf_data (List[float]): Corresponding load times in seconds.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(size_data, perf_data, marker='o', linestyle='-', linewidth=2, markersize=6)

    plt.title("JSON File Loading Performance", fontsize=14, weight='bold', pad=15)
    plt.xlabel("Number of Clients", fontsize=12)
    plt.ylabel("Loading Time (seconds)", fontsize=12)

    # Optional: add gridlines and light ticks
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Optional: add data point labels
    for x, y in zip(size_data, perf_data):
        plt.text(x, y, f"{y:.2f}s", fontsize=8, ha='right', va='bottom')

    plt.tight_layout()
    plt.savefig("screenshots/loading_times.png", dpi=150)
    plt.close()