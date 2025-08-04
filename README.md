# Fly Guy - Flight Record Manager
##  Group Project (Group A) | University of Liverpool
### MSc Data Science and Artificial Intelligence - Software Development module 

<strong>Fly Guy</strong> was created as a group project for the Software Development module at the University of Liverpool. This application provides a user-friendly interface for travel agents to manage client, airline, and flight information efficiently. Written purely in Python.

---

## Table of Contents

- [Fly Guy - Flight Record Manager](#fly-guy---flight-record-manager)
  - [Group Project (Group A) | University of Liverpool](#group-project-group-a--university-of-liverpool)
    - [MSc Data Science and Artificial Intelligence - Software Development module](#msc-data-science-and-artificial-intelligence---software-development-module)
  - [Table of Contents](#table-of-contents)
  - [Why NiceGUI?](#why-nicegui)
  - [Main Functionality](#main-functionality)
    - [Public Flight Search](#public-flight-search)
    - [Secure Agent Portal](#secure-agent-portal)
    - [Client Management](#client-management)
    - [Airline Management](#airline-management)
    - [Flight Management](#flight-management)
    - [Available Flight Management](#available-flight-management)
  - [Potential Future Features](#potential-future-features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributors](#contributors)

---

## Why NiceGUI?

For this project, we needed a way to create a web-based user interface without delving into the complexities of frontend frameworks like React or Angular. Our goal was to build a robust and interactive application primarily using Python. **NiceGUI** emerged as the perfect solution for several key reasons:

* **Pure Python Development**: NiceGUI allows for the creation of web interfaces using only Python. This streamlined our development process, enabling us to focus on the application's logic rather than juggling multiple languages and frameworks.
* **Ease of Use**: The library is known for its gentle learning curve. We were able to quickly build complex, interactive UI components, such as tabs, dialogs, and data tables, with minimal code.
* **Component-Based Architecture**: It offers a rich set of pre-built UI elements (buttons, inputs, tables, etc.) that are both easy to implement and customise. This component-based approach made our code more modular, readable, and maintainable.
* **Built-in Web Server**: NiceGUI handles the web server and backend-frontend communication out of the box, abstracting away the complexities of web development and allowing us to concentrate on the application's features.
* **Rapid Prototyping and Iteration**: The live reload feature was invaluable during development, allowing us to see changes instantly without manually restarting the server.

Ultimately, NiceGUI empowered us to deliver a feature-rich web application on a tight schedule, leveraging our existing Python knowledge to build a professional and responsive user interface.

---

## Main Functionality

The application is a comprehensive record management system for a travel agency. It is split into a public-facing search and a secure agent-only dashboard.

### Public Flight Search

The initial view of the application is a split-screen layout. The right side is dedicated to a public flight search. Any user can enter a `Client ID` and an `Airline ID` to search for booked flights.

### Secure Agent Portal

The left side of the screen features a secure login for travel agents (`Username: admin`, `Password: admin`). Upon successful authentication, the agent is taken to a comprehensive dashboard for managing the agency's records.

### Client Management

Within the agent dashboard, the "Clients" tab allows for full CRUD (Create, Read, Update, Delete) operations for client records. Agents can:
* **Create Client**: Add new clients with details like name, address, and contact information.
* **View/Search Client**: View all clients or search for a specific client by their ID.
* **Edit Client**: Modify the details of existing clients.
* **Delete Client**: Remove a client and all their associated flights from the system.

### Airline Management

The "Airlines" tab provides complete management capabilities for airline companies. Agents can:
* **Create Airline**: Add new airlines to the system.
* **View/Search Airline**: View all airlines or search for a specific airline by its ID.
* **Edit Airline**: Update airline company names.
* **Delete Airline**: Remove an airline and all associated flights.

### Flight Management

The "Flights" tab is the core of the booking system and so the tabs reference "Bookings" rather than flights. It allows agents to:
* **Create Booking**: Book a new flight by selecting an existing client and a Flight ID which will autopopulate the airline, date and travel cities
* **View/Search Bookings**: View all booked flights or filter them by a specific Booking ID.
* **Edit Bookings**: Modify the details of an existing flight booking.
* **Delete Bookings**: Cancel a specific flight booking for a client.

### Available Flight Management

The "Available Flight" tab provides complete management capabilities for available flights. It allows agents to:
* **Create Available Flight**: Create a new available flight by selecting an airline, and specifying the date and travel cities.
* **View/Search Available Flights**: View all available filter them by a specific Flight ID.
* **Edit Available Flights**: Modify the details of an existing available flight.
* **Delete Available Flights**: Remove a specific available available flight.

---

## Potential Future Features
While the current application meets all the project requirements, several features could be implemented to transition it into a production-ready system.

- <strong>Robust Authentication and Authorization</strong>:
    - Replace the hardcoded admin:admin credentials with a proper user database and password hashing (e.g., using passlib).
    - Implement role-based access control (RBAC) to differentiate between agents and administrators.

- <strong>Dedicated Client Portal</strong>:
    - Develop a separate login system for clients. 
    - Allow clients to view their booking history, check flight statuses, and manage their personal information without needing to contact an agent.

- <strong>Database Integration</strong>:
    - Migrate data storage from local JSON files to a relational database like PostgreSQL or a NoSQL database like MongoDB. This would improve data integrity, scalability, and performance.

- <strong>Enhanced Agent Dashboard</strong>:
    - Implement advanced search and filtering capabilities within the "View" tabs (e.g., search clients by name, filter flights by date range). 
    - Add pagination to the data tables to handle a large number of records efficiently.

- <strong>Third-Party API Integration</strong>:
    - Connect to external airline APIs (Global Distribution Systems - GDS) to fetch real-time flight availability and pricing, rather than manually creating airline records.

- <strong>Use of Containers </strong>:
    - Create a Dockerfile to containerise the application, simplifying deployment and ensuring a consistent running environment across different machines.

<strong> and more...</strong>

---

## Installation

To run this project locally, you will need Python 3.8 or higher.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/parduckids/mfa-group-a.git
    cd mfa-group-a
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt 
    ```

---

## Usage

To start the application, navigate to the `src` directory and run the `main.py` file from your terminal:

```bash
cd src
python main.py
```

## Contributors
- [Brendon James Carson](https://github.com/brendoncarson) | <strong>GUI / UX designer</strong>
- [Ismail Ghafoor](https://github.com/Vozsco) | <strong>Programmer</strong>
- [Georgi Hristov](https://github.com/Gesh94) | <strong>Tester</strong>
- [Elvis Kinoti Muthuri](https://github.com/ElvisKM) | <strong>Project Manager</strong>
- [Adam Voros](https://github.com/parduckids) | <strong>Project Manager / Programmer</strong>