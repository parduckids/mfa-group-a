# Test Suite Overview

This document provides an overview of the testing approach for this project, how to run the tests, and the rationale behind the structure and tools used.

---

## What’s Covered

The test suite is designed to verify the functionality of the NiceGUI web application. It covers:

- Home page view and functionalities
- Authentication (login/logout)
- Agent Dashboard (create, view, edit, delete)
  - visibility of the correct tabs
  - ability to create, view, edit and delete records
- UI-level behaviors using Selenium and `nicegui.testing.Screen`

---

## How the Tests Are Structured

All test files are located in the `tests/` folder and follow a modular structure:

```bash
tests/
├── conftest.py              # Shared fixtures
├── utils.py                 # Shared utility functions
├── test_load_save_json.py   # Tests for loading/saving JSON files
├── test_home_screen.py      # Home screen appearance and functionality
├── test_flight_search.py    # Flight search section functionality
├── test_login.py            # Login/logout functionality
├── test_after_login_tabs.py # Tab visibility checks after login
├── test_create.py           # Create clients, airlines, bookings, flights
├── test_view.py             # View clients, airlines, bookings, flights
├── test_edit.py             # Edit clients, airlines, bookings, flights
├── test_delete.py           # Delete clients, airlines, bookings, flights
├── test_json_load_speed.py  # Load speed of json files of different sizes
```
Each file groups related functionality for maintainability and clarity. This also enables selective execution of test groups during development.

## Tools Used

- **pytest**: Test runner and assertion framework
- **Selenium (via NiceGUI)**: To simulate user interaction with the UI
- **NiceGUI's `Screen` helper**: Simplifies locating elements and running browser-based tests
- **pytest-order**: Used to control the order of execution of the tests
- **matplotlib**: Used for graph generation

---

## How to Run the Tests

#### To run all tests:

To run all test files in the specified order:

```bash
pytest src
```
To run a specific test folder:

```bash
pytest src/tests/
```
To run a specific test file:

```bash
pytest src/tests/test_client_create.py
```

To run any of the above commands with more detailed log output:

```bash
pytest -s
```

Test Lifecycle
Each test opens the app, performs UI actions (like filling forms or clicking buttons), and asserts visible outcomes (such as notifications, table contents, or tab visibility).

#### Where needed, tests:

Use `screen.wait()` to ensure dynamic elements are ready.

Use `aria-label` or custom data attributes for reliable input selection.

Take screenshots after completion to capture the state of the app at the end of the test.

The `load_speed_json` test does not interact with the UI but measures JSON loading performance across varying dataset sizes and saves a performance graph to the screenshots folder.

#### How Data Is Handled
Some tests create dummy records (e.g., clients or flights). 

Where possible tests clean up after themselves (e.g., delete test records).

The `load_speed_json` test generates a temporary JSON file with dummy client data, which are deleted after each run.

Shared fixtures can be added in `conftest.py` for reusability and cleanup hooks.

Shared functions exist in `utils.py` for reusability and modularity.

Test order is set with the purpose to allow for tests to create, view, edit and delete their own dummy data. However, they are written in such a way that they can be run independently and individually as well.

#### Benefits of This Approach
- Clear test boundaries (grouped by functionality)
- Readable, maintainable code
- Reusable setup and teardown logic
- Tests mimic real user behavior through the UI
- Easily debuggable with visual output

#### Limitations
- UI tests are slower than unit tests due to browser interaction
- Dynamic content (e.g. modals or dialogs) may require additional wait logic
- If validation logic runs on blur or keypress, tests may need to simulate real typing carefully

#### Output Files
Screenshots of all tests and a graph of the `test_json_load_speed` test are saved in `src/screenshots/`

#### Cleanup and Maintenance
- Keep test data separate from production data
- Clean up test-created records when possible
- Periodically review old screenshots in src/screenshots/

#### Suggested Improvements
- <strong>Modularize Repeated Logic</strong>:
  - Extract further common actions (e.g. tab navigation, input clearing, button filtering) into helper functions to reduce duplication and improve readability.

- <strong>Use Parametrization</strong>:
  - Apply `@pytest.mark.parametrize` to consolidate similar tests with varying inputs (e.g. login errors, search results).

- <strong>Improve Test Coverage</strong>:
  - Include edge cases (e.g. empty datasets, max input lengths) and negative tests (e.g. unauthorized access).

- <strong>Group Tests by Feature</strong>:
  - Organize tests into files/folders by entity (e.g. clients/, airlines/) for easier navigation and scalability.

- <strong>Use Constants for Static Text</strong>:
  - Store repeated strings (e.g. button labels, messages) in a constants module to reduce typos and simplify updates.

- <strong>Add Accessibility Selectors</strong>:
  - Prefer `aria-label` or roles over text content when locating elements, where possible, for stability and accessibility.

- <strong>Test Performance at Scale</strong>:
  - Add tests with large datasets to measure UI responsiveness, load time, and search/filter speed. Use fixtures to simulate heavy usage and assert performance thresholds.

#### Final Notes
This test suite ensures our app works as expected from a user’s perspective. It’s a valuable part of preventing regressions and ensuring that changes to logic or UI don’t silently break existing features.