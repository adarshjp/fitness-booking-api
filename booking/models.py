from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    instructor = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()

    def __str__(self):
        return f"{self.name} by {self.instructor} at {self.start_time}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"
