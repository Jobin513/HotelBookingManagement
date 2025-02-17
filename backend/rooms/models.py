from django.db import models


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]

    ROOM_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Under Maintenance', 'Under Maintenance'),
    ]

    room_number = models.CharField(max_length=50)  # Alphanumeric room number
    type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=ROOM_STATUS_CHOICES)
    capacity = models.PositiveIntegerField()  # Ensure capacity is positive
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    last_changed_by = models.CharField(max_length=100, blank=True, null=True)
    last_changed_date = models.DateTimeField(auto_now=True)  # Automatically set when updated

    def __str__(self):
        return f"Room {self.room_number} - {self.type}"
