from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from rest_framework import status
from .models import FitnessClass, Booking
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .serializers import FitnessClassSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_classes(request):
    """
    Retrieve all fitness classes.
    This endpoint returns a list of all available fitness classes with their details.
    """
    logger.info("Attempting to retrieve all fitness classes.")
    classes = FitnessClass.objects.all()
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    """
    Book a fitness class.
    This endpoint checks if there are available slots before creating a booking.
    """
    logger.info(f"Booking attempt received with data: {request.data}")
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        class_id = request.data.get('fitness_class')
        client_email = request.data.get('client_email') # Get email for logging
        try:
            with transaction.atomic():
                fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)
                logger.info(f"Found class ID {class_id} for booking by {client_email}.")
                if fitness_class.available_slots > 0:
                    fitness_class.available_slots = F('available_slots') - 1
                    fitness_class.save(update_fields=['available_slots'])
                    serializer.save()
                    logger.info(f"Successfully booked class ID {class_id} for {client_email}. Remaining slots: {fitness_class.available_slots}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    logger.warning(f"Booking failed for class ID {class_id} by {client_email}: No slots available.")
                    return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)
        except FitnessClass.DoesNotExist:
            logger.error(f"Booking failed for class ID {class_id} by {client_email}: Class not found.")
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Unexpected error during booking for class ID {class_id} by {client_email}: {e}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_bookings_by_email(request):
    """
    Retrieve bookings by client email.
    This endpoint allows clients to view their bookings by providing their email.    
    Requires 'email' query parameter.
    """
    email = request.GET.get("email")
    logger.info(f"Attempting to retrieve bookings for email: {email}")
    if not email:
        logger.warning("Attempt to get bookings without providing an email parameter.")
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_email(email)
    except ValidationError:
        logger.warning(f"Invalid email format provided for booking retrieval: {email}")
        return Response({"error": "Invalid email format provided."}, status=status.HTTP_400_BAD_REQUEST)


    bookings = Booking.objects.filter(client_email=email)
    logger.info(f"Found {bookings.count()} bookings for email: {email}")
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
