import pytest
from app.startup import *
import json
from pathlib import Path

@pytest.mark.order(1)
def test_load_json_no_path(tmp_path):
    """
    Test that loading a non-existent JSON file returns the provided default.

    This test verifies that:
        - If the file does not exist, the function returns the default value
        - The default value in this case is an empty dictionary

    Args:
        tmp_path (Path): Pytest fixture for creating a temporary directory.
    """
    # Create a temp file using pytest fixture
    path = tmp_path / "missing.json"
    
    # Load the function and test the result
    result = load_json(path, default=dict)
    assert result == {}
    
@pytest.mark.order(2)
def test_load_json_path(tmp_path):
    """
    Test that loading an existing JSON file returns the correct data.

    This test verifies that:
        - The data saved in the file is correctly deserialized by load_json

    Args:
        tmp_path (Path): Pytest fixture for creating a temporary directory.
    """
    # Create a temp file using pytest fixture
    path = tmp_path / "data.json"
    
    # Create dummy data and dump into the temp file
    data = {'test_key': "test_value"}
    path.write_text(json.dumps(data))
    
    # Load the function and test the output
    result = load_json(path)
    assert result == data
    
@pytest.mark.order(3)
def test_save_json(tmp_path, monkeypatch):
    """
    Test that save_json correctly writes data to a file.

    This test verifies that:
        - The JSON file is created at the correct path
        - The contents of the file match the original data
        - The global data_dir is temporarily patched to the test path

    Args:
        tmp_path (Path): Pytest fixture for creating a temporary directory.
        monkeypatch (MonkeyPatch): Pytest fixture to modify module attributes.
    """
    # Override the global variable 
    monkeypatch.setattr('app.startup.data_dir', tmp_path)
    
    # Create a temp file using pytest fixture
    path = tmp_path / "data.json"
    
    # Create dummy data and dump into the temp file
    data = {'test_key': "test_value"}
    save_json(path, data)
    
    # Load the function and test the output
    assert path.exists()
    assert json.loads(path.read_text()) == data