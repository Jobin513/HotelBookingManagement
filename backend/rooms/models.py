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








    """
    @property
    def is_room_available(self, check_in, check_out):

        Checks if the room is available for the given check-in and check-out dates.

        :param check_in: The check-in date (datetime object)
        :param check_out: The check-out date (datetime object)
        :return: Boolean availability and error message if any

        try:
            from bookings.models import Booking
            # Ensure room exists (the room object is already available in `self`).
            if not self:
                raise ValidationError("Error: Room ID is required.")

            if not isinstance(check_in, datetime) or not isinstance(check_out, datetime):
                raise ValidationError("Error: Check-in and check-out must be valid datetime objects.")

            # Ensure the dates are not in the past
            current_date = datetime.now()
            if check_in < current_date or check_out < current_date:
                raise ValidationError("Error: Check-in and check-out dates must not be in the past.")

            # Ensure check_in date is before check_out date
            if check_in >= check_out:
                raise ValidationError("Error: Check-in date must be before check-out date.")

            # Ensure booking duration is within limits (example: 14 days maximum)
            max_days_allowed = 14
            if (check_out - check_in).days > max_days_allowed:
                raise ValidationError(f"Error: The maximum booking duration is {max_days_allowed} days.")

            # Check if room is booked or under maintenance
            if self.room_status == "Booked":
                raise ValidationError("Error: Room is already booked for the selected dates.")
            if self.room_status == "Under Maintenance":
                raise ValidationError("Error: Room is currently under maintenance and cannot be booked.")

            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                room=self,
                check_in__lt=check_out,  # Booking starts before check-out date
                check_out__gt=check_in  # Booking ends after check-in date
            )

            if overlapping_bookings.exists():
                raise ValidationError("Error: Room is unavailable for the selected dates.")

            # If no issues, return True indicating the room is available
            return True

        except ValidationError as e:
            # Return False and the error message
            return False, str(e)
    """
    def __str__(self):

        return f"Room {self.room_number} - {self.room_type}"
