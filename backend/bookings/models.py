from datetime import date

from django.db import models

from guests.models import Guest
from pydantic_core import ValidationError
from rooms.models import Room


class Booking(models.Model):
    class Meta:
        app_label = 'bookings'
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    booking_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    payment_status = models.BooleanField(default=False)  # True if paid, False if not
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    def clean(self):
        # Case 1: Ensure that check_in is before check_out
        if self.check_in >= self.check_out:
            raise ValidationError("Check-in date must be before the check-out date.")
        # Case 2: Ensure room is available between the given dates
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        )
        if overlapping_bookings.exists():
            raise ValidationError("The room is already booked for the selected dates.")
        # Case 3: Validate the total_price
        if self.total_price < 50:
            raise ValidationError("Total price cannot be less than 50.")
        if self.total_price > 500:
            raise ValidationError("Total price cannot be more than 500.")
        # Case 4: Validate the guest and room status
        if self.status not in ['booked', 'available', 'under maintenance']:
            raise ValidationError("Invalid room status. Must be booked, available, or under maintenance.")
        # Case 5: Validate that check_in and check_out dates are not in the past
        if self.check_in < date.today():
            raise ValidationError("Check-in date cannot be in the past.")
        # Case 6: Check if the room is available for booking
        if not self.room.status == 'Available':
            raise ValidationError("Room is not available for booking.")
        # Additional case: Room status shouldn't be "booked" or "under maintenance" if it's not available
        if self.room.status == 'booked' and self.check_in >= self.room.booked_until:
            raise ValidationError("Room cannot be booked for the requested dates.")
        # Case 7: Ensure the guest exists
        if not Guest.objects.filter(id=self.guest.id).exists():
            raise ValidationError("Guest does not exist.")

    def __str__(self):
        return f"Booking {self.booking_id} - {self.guest.name} ({self.status})"
