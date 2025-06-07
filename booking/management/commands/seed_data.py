# e:\fitness-booking-api\booking\management\commands\seed_data.py
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from booking.models import FitnessClass, Booking # Import Booking if you want to seed bookings too

class Command(BaseCommand):
    help = 'Seeds the database with initial sample data for fitness classes and bookings.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

        # Clear existing data (optional, be careful with this in production)
        # You might want to add a command-line flag to control this
        if options.get('clear', False): # Example: add --clear flag
            self.stdout.write(self.style.WARNING('Clearing existing FitnessClass and Booking data...'))
            Booking.objects.all().delete()
            FitnessClass.objects.all().delete()

        # Create Fitness Classes
        classes_data = [
            {
                "name": "Morning Yoga Flow",
                "instructor": "Aisha Sharma",
                "start_time": now() + timedelta(days=1, hours=2), # Tomorrow at 9 AM (assuming TZ is set)
                "total_slots": 20,
                "available_slots": 18
            },
            {
                "name": "HIIT Blast",
                "instructor": "Raj Patel",
                "start_time": now() + timedelta(days=1, hours=11), # Tomorrow at 6 PM
                "total_slots": 15,
                "available_slots": 15
            },
            {
                "name": "Evening Pilates",
                "instructor": "Priya Singh",
                "start_time": now() + timedelta(days=2, hours=12), # Day after tomorrow at 7 PM
                "total_slots": 12,
                "available_slots": 10
            },
            {
                "name": "Weekend Zumba Party",
                "instructor": "Carlos Rodriguez",
                "start_time": now() + timedelta(days=(6 - now().weekday() + 7) % 7 + 1, hours=3), # Next Saturday at 10 AM
                "total_slots": 25,
                "available_slots": 25
            },
            {
                "name": "Strength Training 101",
                "instructor": "David Lee",
                "start_time": now() + timedelta(days=3, hours=10),
                "total_slots": 10,
                "available_slots": 5 # Partially booked
            }
        ]

        created_classes = []
        for class_data in classes_data:
            fitness_class, created = FitnessClass.objects.get_or_create(
                name=class_data["name"],
                instructor=class_data["instructor"],
                defaults=class_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created FitnessClass: {fitness_class.name}'))
                created_classes.append(fitness_class)
            else:
                self.stdout.write(self.style.NOTICE(f'FitnessClass already exists: {fitness_class.name}'))


        if created_classes:
            bookings_data = [
                {
                    "fitness_class": created_classes[0] if len(created_classes) > 0 else None,
                    "client_name": "Alice Wonderland",
                    "client_email": "alice@example.com"
                },
                {
                    "fitness_class": created_classes[4] if len(created_classes) > 4 else None,
                    "client_name": "Bob The Builder",
                    "client_email": "bob@example.com"
                }
            ]

            for booking_data in bookings_data:
                if booking_data["fitness_class"]:
                    booking, created = Booking.objects.get_or_create(
                        fitness_class=booking_data["fitness_class"],
                        client_email=booking_data["client_email"],
                        defaults={"client_name": booking_data["client_name"]}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created Booking for {booking.client_name} in {booking.fitness_class.name}'))
                    else:
                        self.stdout.write(self.style.NOTICE(f'Booking for {booking_data["client_name"]} in {booking_data["fitness_class"].name} already exists.'))

        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing FitnessClass and Booking data before seeding.',
        )