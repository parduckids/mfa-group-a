import pytest
import json
from tests.utils import test_clients_file
import time
import matplotlib.pyplot as plt

parameters = [10, 50, 100, 500, 1000, 2500, 5000, 7500, 10000, 20000, 40000, 60000, 80000, 10000]
size_data = []
perf_data = []

@pytest.mark.parametrize(
    'test_clients_file', 
    parameters, 
    indirect=True
)
def test_loading_speed(test_clients_file):
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
    plt.figure(figsize=(10, 6))
    plt.plot(size_data, perf_data, marker='o')
    plt.title("JSON Client File Loading Time vs File Size")
    plt.xlabel("Number of Clients")
    plt.ylabel("Loading Time (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("screenshots/loading_times.png")
    #plt.show()