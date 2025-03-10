import decimal
from datetime import datetime
from decimal import Decimal

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

    id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50, unique=True)  # Alphanumeric room number
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    room_status = models.CharField(max_length=50, choices=ROOM_STATUS_CHOICES)
    capacity = models.PositiveIntegerField()  # Ensure capacity is positive
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    last_changed_by = models.CharField(max_length=100, blank=True, null=True)
    last_changed_date = models.DateTimeField(auto_now=True)  # Automatically set when updated

    # Room Model related validation error raised messages
    def clean(self):
        if self.room_type not in dict(self.ROOM_TYPE_CHOICES):
            raise ValidationError("Invalid room type. Must be Single, Double, or Suite.")
        if self.room_status not in dict(self.ROOM_STATUS_CHOICES):
            raise ValidationError("Invalid room status. Must be Available, Booked, or Under Maintenance")
        if self.rate > Decimal("500.00"):
            raise ValidationError("Room could not be created. Price cannot be more than 500.00.")
        if self.rate < Decimal("50.00"):
            raise ValidationError("Room could not be created. Price cannot be less than 50.00.")
        if self.rate is None:
            raise ValidationError("Price cannot be empty.")
        if self.rate is decimal:
            raise ValidationError("Price must be a decimal.")
        if not isinstance(self.capacity, int):
            raise ValidationError("Room capacity must be an integer.")
        if isinstance(self.capacity, float) and self.capacity.is_integer() is False:
            raise ValidationError("Room capacity must be an integer.")
        if self.capacity < 1:
            raise ValidationError("Room capacity must be at least 1.")
        if self.capacity > 5:  # Assuming 5 is the maximum allowed capacity
            raise ValidationError("Room capacity cannot exceed 5.")
        super().clean()

    def is_room_available(self, check_in, check_out, room_id):
        """
        Checks if the room is available for the given check-in and check-out dates.

        :param check_in: The check-in date (datetime object)
        :param check_out: The check-out date (datetime object)
        :param room_id: The ID of the room to check availability for
        :return: Tuple (boolean availability, error message if any)
        """
        try:
            from bookings.models import Booking
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            print("Error: Room ID not found in the database.")
            return False

        if room_id is None:
            print("Error: Room ID is required.")
            return False

        if not isinstance(check_in, datetime) or not isinstance(check_out, datetime):
            print("Error: Check-in and check-out must be valid date objects.")
            return False

        current_date = datetime.now()
        if check_in < current_date or check_out < current_date:
            print("Error: Check-in and check-out dates must not be in the past.")
            return False

        if check_in >= check_out:
            print("Error: Check-in date must be before check-out date.")
            return False

        max_days_allowed = 14
        if (check_out - check_in).days > max_days_allowed:
            print(f"Error: The maximum booking duration is {max_days_allowed} days.")
            return False

        if room.room_status == "Booked":
            print("Error: Room is already booked for the selected dates.")
            return False

        if room.room_status == "Under Maintenance":
            print("Error: Room is currently under maintenance and cannot be booked.")
            return False

        existing_bookings = Booking.objects.filter(
            room_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        if existing_bookings.exists():
            print("Error: Room is unavailable for the selected dates.")
            return False

        return True

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"
