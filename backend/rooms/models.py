from django.core.exceptions import ValidationError
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

    # Room Model related validation error raised messages
    def clean(self):
        if self.type not in dict(self.ROOM_TYPE_CHOICES):
            raise ValidationError("Invalid room type. Must be Single, Double, or Suite.")
        if self.status not in dict(self.ROOM_STATUS_CHOICES):
            raise ValidationError("Invalid room status. Must be Available, Booked, or Under Maintenance")
        if not isinstance(self.capacity, int):
            raise ValidationError("Room capacity must be an integer.")
        if isinstance(self.capacity, float) and self.capacity.is_integer() is False:
            raise ValidationError("Room capacity must be an integer.")
        if self.capacity < 1:
            raise ValidationError("Room capacity must be at least 1.")
        if self.capacity > 5:  # Assuming 5 is the maximum allowed capacity
            raise ValidationError("Room capacity cannot exceed 5.")
        super().clean()

    def __str__(self):
        return f"Room {self.room_number} - {self.type}"
