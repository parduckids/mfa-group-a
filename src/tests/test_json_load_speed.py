import pytest
import json
from tests.utils import test_json_file
import time
import matplotlib.pyplot as plt
from pathlib import Path

template_types = ['clients', 'flights', 'airlines', 'available_flights']
parameters = [100, 1000, 10000, 30000, 60000, 100000]
perf_results = {
    t: {
        "sizes": [],       
        "durations": [],    
        "file_sizes": []
    }
    for t in template_types
}

@pytest.mark.order(31)
@pytest.mark.parametrize(
    'test_json_file', 
    [(p, 'clients') for p in parameters],
    indirect=True
)
def test_loading_speed_clients(test_json_file):
    """
    Performance test for measuring JSON client file loading speed.

    This test benchmarks how long it takes to load a JSON file containing a
    varying number of client records. It verifies that:
        - The JSON file can be successfully opened and parsed
        - The loading time and file size are recorded and printed

    After the last test case (largest dataset), a performance graph is generated.

    Args:
        test_json_file (Path): Path to the generated JSON file with client data.
    """
    start = time.perf_counter()

    with open(test_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    end = time.perf_counter()
    duration = end - start

    # Extract info
    input_size = int(test_json_file.stem.split('_')[-1])
    file_size_mb = test_json_file.stat().st_size / (1024 * 1024)  # MB

    # Store results
    perf_results['clients']['sizes'].append(input_size)
    perf_results['clients']['durations'].append(duration)
    perf_results['clients']['file_sizes'].append(file_size_mb)
    
    if input_size == max(parameters):
        generate_dual_axis_plot(
            perf_results['clients']['sizes'],
            perf_results['clients']['durations'],
            perf_results['clients']['file_sizes'],
            'clients'
        )

@pytest.mark.order(32)
@pytest.mark.parametrize(
    'test_json_file', 
    [(p, 'flights') for p in parameters],  # Use 'flights' template
    indirect=True
)
def test_loading_speed_flights(test_json_file):
    """
    Performance test for measuring JSON flight file loading speed.

    This test benchmarks how long it takes to load a JSON file containing a
    varying number of flight records. It verifies that:
        - The JSON file can be successfully opened and parsed
        - The number of records matches the test parameter
        - The loading time is recorded for performance plotting

    After the last test case (largest dataset), a performance graph is generated.

    Args:
        test_json_file (Path): Path to the generated JSON file with flight data.
    """
    start = time.perf_counter()

    with open(test_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    end = time.perf_counter()
    duration = end - start

    input_size = int(test_json_file.stem.split('_')[-1])
    file_size_mb = test_json_file.stat().st_size / (1024 * 1024)

    perf_results['flights']['sizes'].append(input_size)
    perf_results['flights']['durations'].append(duration)
    perf_results['flights']['file_sizes'].append(file_size_mb)

    if input_size == max(parameters):
        generate_dual_axis_plot(
            perf_results['flights']['sizes'],
            perf_results['flights']['durations'],
            perf_results['flights']['file_sizes'],
            'flights'
        )
        
@pytest.mark.order(33)
@pytest.mark.parametrize(
    'test_json_file', 
    [(p, 'airlines') for p in parameters],  # Use 'airlines' template
    indirect=True
)
def test_loading_speed_airlines(test_json_file):
    """
    Performance test for measuring JSON airline file loading speed.

    This test benchmarks how long it takes to load a JSON file containing a
    varying number of airline records. It verifies that:
        - The JSON file can be successfully opened and parsed
        - The number of records matches the test parameter
        - The loading time is recorded for performance plotting

    After the last test case (largest dataset), a performance graph is generated.

    Args:
        test_json_file (Path): Path to the generated JSON file with airline data.
    """
    start = time.perf_counter()

    with open(test_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    end = time.perf_counter()
    duration = end - start

    # Extract info
    input_size = int(test_json_file.stem.split('_')[-1])
    file_size_mb = test_json_file.stat().st_size / (1024 * 1024)

    perf_results['airlines']['sizes'].append(input_size)
    perf_results['airlines']['durations'].append(duration)
    perf_results['airlines']['file_sizes'].append(file_size_mb)

    if input_size == max(parameters):
        generate_dual_axis_plot(
            perf_results['airlines']['sizes'],
            perf_results['airlines']['durations'],
            perf_results['airlines']['file_sizes'],
            'airlines'
        )

@pytest.mark.order(34)
@pytest.mark.parametrize(
    'test_json_file', 
    [(p, 'available_flights') for p in parameters],  # Use 'available_flights' template
    indirect=True
)
def test_loading_speed_available_flights(test_json_file):
    """
    Performance test for measuring JSON available_flights file loading speed.

    This test benchmarks how long it takes to load a JSON file containing a
    varying number of available flight records. It verifies that:
        - The JSON file can be successfully opened and parsed
        - The number of records matches the test parameter
        - The loading time is recorded for performance plotting

    After the last test case (largest dataset), a performance graph is generated.

    Args:
        test_json_file (Path): Path to the generated JSON file with available flight data.
    """
    start = time.perf_counter()

    with open(test_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    end = time.perf_counter()
    duration = end - start
    
    # Extract info
    input_size = int(test_json_file.stem.split('_')[-1])
    file_size_mb = test_json_file.stat().st_size / (1024 * 1024)

    perf_results['available_flights']['sizes'].append(input_size)
    perf_results['available_flights']['durations'].append(duration)
    perf_results['available_flights']['file_sizes'].append(file_size_mb)

    if input_size == max(parameters):
        generate_dual_axis_plot(
            perf_results['available_flights']['sizes'],
            perf_results['available_flights']['durations'],
            perf_results['available_flights']['file_sizes'],
            'available_flights'
        )

def generate_dual_axis_plot(size_data, durations, file_sizes, template_type: str):
    """
    Generate and save a dual-axis plot: Load time (s) and file size (MB) vs number of records,
    with annotations showing both values at each point — styled to match their axes.

    Args:
        size_data (List[int]): Number of records (X-axis).
        durations (List[float]): Load times in seconds (Y1-axis).
        file_sizes (List[float]): File sizes in MB (Y2-axis).
        template_type (str): Type of data for the title/filename.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Load Time (Y1)
    color1 = 'tab:blue'
    ax1.set_xlabel('Number of Records', fontsize=12)
    ax1.set_ylabel('Load Time (seconds)', color=color1, fontsize=12)
    ax1.plot(size_data, durations, color=color1, marker='o', label='Load Time', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)

    # Plot File Size (Y2)
    ax2 = ax1.twinx()
    color2 = 'tab:green'
    ax2.set_ylabel('File Size (MB)', color=color2, fontsize=12)
    ax2.plot(size_data, file_sizes, color=color2, marker='s', linestyle='--', label='File Size', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color2)

    # Title and Grid
    plt.title(f"{template_type.replace('_', ' ').title()} JSON Loading Performance", fontsize=14, weight='bold', pad=15)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Annotate points with more spacing
    for x, y1, y2 in zip(size_data, durations, file_sizes):
        ax1.text(
            x, y1 + (max(durations) * 0.03),  # move text higher above
            f"{y1:.2f}s", fontsize=8, ha='center', va='bottom', color=color1
        )
        ax1.text(
            x, y1 - (max(durations) * 0.06),  # move text further below
            f"{y2:.2f}MB", fontsize=8, ha='center', va='top', color=color2
        )
    # Save the plot
    plt.tight_layout()
    screenshots_dir = Path(__file__).resolve().parent.parent.parent / 'screenshots'
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    plot_filename = screenshots_dir / f"{template_type}_dual_axis_performance.png"
    plt.savefig(plot_filename, dpi=150)
    plt.close()
