# Fitness Class Booking API

This project is a Django-based API for managing and booking fitness classes.

## Features

*   List available fitness classes.
*   Book a fitness class for a client.
*   View bookings for a specific client by email.

## Prerequisites

*   Python 3.10 or higher
*   pip (Python package installer)
*   Git

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/adarshjp/fitness-booking-api.git
    cd fitness-booking-api
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows (Git Bash or similar):
        ```bash
        python -m venv venv
        source venv/Scripts/activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```
## Seeding the Database (Optional)

The project includes a command to seed the database with sample fitness classes and bookings. This is useful for development and testing.

1.  **Seed initial data:**
    ```bash
    python manage.py seed_data
    ```

2.  **To clear existing data before seeding (use with caution):**
    ```bash
    python manage.py seed_data --clear
    ```
    This will delete all existing `FitnessClass` and `Booking` records before adding the new sample data.

## Running the Development Server

Once the setup is complete, you can run the Django development server:

```bash
python manage.py runserver
```

The API will typically be available at `http://127.0.0.1:8000/`.

## Running Tests

To run the automated tests for the application, use `pytest`:

```bash
(venv) $ pytest
```

Make sure your virtual environment is activated.

## API Endpoints

The API is typically available at `http://127.0.0.1:8000/`. All endpoints below are prefixed with `/api/`.

*   **`GET /api/classes/`**
    *   Retrieves a list of all available fitness classes.
    *   **Example cURL:**
        ```bash
        curl -X GET http://127.0.0.1:8000/api/classes/
        ```

*   **`POST /api/book/`**
    *   Books a fitness class for a client.
    *   **Request Body (JSON):**
        ```json
        {
            "fitness_class": 1,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        ```
    *   **Example cURL:**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/book/ \
        -H "Content-Type: application/json" \
        -d '{"fitness_class": 1, "client_name": "John Doe", "client_email": "john@example.com"}'
        ```

*   **`GET /api/bookings/`**
    *   Retrieves bookings for a specific client.
    *   Requires an `email` query parameter (e.g., `/api/bookings/?email=john@example.com`).
    *   **Example cURL:**
        ```bash
        curl -X GET "http://127.0.0.1:8000/api/bookings/?email=john@example.com"
        ```

### Using Postman

You can also use tools like Postman to interact with these API endpoints.

1.  Set the request type (GET, POST).
2.  Enter the request URL (e.g., `http://127.0.0.1:8000/api/classes/`).
3.  For POST requests:
    *   Go to the "Body" tab.
    *   Select "raw" and choose "JSON" from the dropdown.
    *   Enter the JSON payload in the text area.
4.  Click "Send".

## Project Structure

*   `fitness_studio/`: Main Django project configuration.
*   `booking/`: Django app handling the booking logic, models, views, and serializers.
*   `manage.py`: Django's command-line utility.
*   `requirements.txt`: Project dependencies.
*   `pytest.ini`: Configuration for pytest.