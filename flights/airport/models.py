from django.db import models

class Flight(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    time = models.TimeField()
    duration = models.DurationField()
    date = models.DateField(null=True)

    total_seats = models.IntegerField(default=30)  # total seats

    def __str__(self):
        return f"{self.origin} → {self.destination} on {self.date} at {self.time}"

class FlightBooking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seat_number = models.IntegerField()
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger_name} booked {self.flight} Seat {self.seat_number}"
