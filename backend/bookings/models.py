
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, datetime
from decimal import Decimal
from guests.models import Guest
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="bookings")
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    check_in = models.DateField()
    check_out = models.DateField()
    payment_status = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        # Case 1: Ensure that check_in date is before check_out date
        if self.check_in >= self.check_out:
            raise ValidationError("Check-in date must be before check-out date.")

        # Case 2: Ensure room availability for the selected dates
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
            booking_status='confirmed'  # Only confirmed bookings should be checked
        )
        # Exclude the current booking if it's being edited
        if self.pk:  # Check if this is an existing booking
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("The room is already booked for the selected dates.")

        # Case 3: Validate the total_price
        if self.total_price < Decimal("50.00"):
            raise ValidationError("Total price cannot be less than 50.")
        if self.total_price > Decimal("500.00"):
            raise ValidationError("Total price cannot be more than 500.")

        # Case 4: Validate the room and guest status
        if self.room.room_status not in ['Available']:
            raise ValidationError("Room is not available for booking.")

        if not Guest.objects.filter(guest_id=self.guest.guest_id).exists():
            raise ValidationError("Guest does not exist.")

        # Case 5: Ensure the check_in date is not in the past
        if self.check_in < date.today():
            raise ValidationError("Check-in date cannot be in the past.")

    def _str_(self):
        return f"Booking {self.booking_id} - {self.guest.first_name} {self.guest.last_name} ({self.booking_status}) ({self.payment_status})"