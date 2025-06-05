from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

@api_view(['GET'])
def get_classes(request):
    classes = FitnessClass.objects.all()
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        class_id = request.data.get('fitness_class')
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
            if fitness_class.available_slots > 0:
                fitness_class.available_slots -= 1
                fitness_class.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "No slots available"}, status=400)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_bookings_by_email(request):
    email = request.GET.get("email")
    bookings = Booking.objects.filter(client_email=email)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
