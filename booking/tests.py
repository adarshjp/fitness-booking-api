import pytest
from rest_framework.test import APIClient
from booking.models import FitnessClass, Booking # Import Booking
from django.utils.timezone import now, timedelta

@pytest.mark.django_db
def test_get_classes_returns_200():
    FitnessClass.objects.create(
        name="Yoga",
        instructor="Anita",
        start_time=now() + timedelta(hours=1),
        total_slots=10,
        available_slots=10
    )
    client = APIClient()
    response = client.get('/api/classes/')
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_booking_success():
    cls = FitnessClass.objects.create(
        name="HIIT",
        instructor="Ravi",
        start_time=now() + timedelta(hours=1),
        total_slots=10,
        available_slots=10
    )
    client = APIClient()
    payload = {
        "fitness_class": cls.id,
        "client_name": "John Doe",
        "client_email": "john@example.com"
    }
    response = client.post('/api/book/', payload, format='json')
    assert response.status_code == 201
    # Check if the available slots were decremented
    cls.refresh_from_db()
    assert cls.available_slots == 9
    # Check if a booking record was created
    assert Booking.objects.filter(client_email="john@example.com", fitness_class=cls).exists()

@pytest.mark.django_db
def test_booking_no_slots():
    cls = FitnessClass.objects.create(
        name="Pilates",
        instructor="Maria",
        start_time=now() + timedelta(hours=2),
        total_slots=1,
        available_slots=0  # No slots available
    )
    client = APIClient()
    payload = {
        "fitness_class": cls.id,
        "client_name": "Jane Doe",
        "client_email": "jane@example.com"
    }
    response = client.post('/api/book/', payload, format='json')
    assert response.status_code == 400
    assert response.data["error"] == "No slots available"

@pytest.mark.django_db
def test_booking_class_not_found():
    client = APIClient()
    non_existent_class_id = 999
    payload = {
        "fitness_class": non_existent_class_id,
        "client_name": "Ghost User",
        "client_email": "ghost@example.com"
    }
    response = client.post('/api/book/', payload, format='json')
    # Serializer validation for non-existent PK results in 400
    assert response.status_code == 400
    # Check for the serializer's error message format
    assert "fitness_class" in response.data 
    assert "Invalid pk" in str(response.data["fitness_class"])

@pytest.mark.django_db
def test_booking_invalid_payload():
    cls = FitnessClass.objects.create(
        name="Zumba",
        instructor="Carlos",
        start_time=now() + timedelta(hours=1),
        total_slots=5,
        available_slots=5
    )
    client = APIClient()
    payload = {
        # Missing fitness_class
        "client_name": "Incomplete User",
        "client_email": "incomplete@example.com"
    }
    response = client.post('/api/book/', payload, format='json')
    assert response.status_code == 400
    assert "fitness_class" in response.data # Serializer error for missing field

@pytest.mark.django_db
def test_get_bookings_by_email():
    cls = FitnessClass.objects.create(name="Spin", instructor="Laura", start_time=now(), total_slots=10, available_slots=10)
    Booking.objects.create(fitness_class=cls, client_name="Test User", client_email="test@example.com")
    Booking.objects.create(fitness_class=cls, client_name="Test User", client_email="test@example.com")

    client = APIClient()
    response = client.get('/api/bookings/?email=test@example.com')
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_get_bookings_by_email_no_bookings():
    client = APIClient()
    response = client.get('/api/bookings/?email=nobody@example.com')
    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db
def test_get_classes_no_classes_returns_200_empty():
    client = APIClient()
    response = client.get('/api/classes/')
    assert response.status_code == 200
    assert len(response.data) == 0
