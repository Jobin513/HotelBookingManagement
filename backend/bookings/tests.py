from django.core.exceptions import ValidationError
from django.test import TestCase
from bookings.models import Booking
from rooms.models import Room
from guests.models import Guest
from datetime import date, datetime


class BookingTest(TestCase):

    def setUp(self):
        """Set up test data for Is_Room_Available tests"""
        # Valid room under Maintenance
        self.room1 = Room.objects.create(
            room_number="101A",
            room_type="Single",
            rate=50.00,
            room_status="Maintenance",
            capacity=2
        )

        # Valid room under Available
        self.room2 = Room.objects.create(
            room_number="102B",
            room_type="Double",
            rate=75.00,
            room_status="Available",
            capacity=4
        )

        # Room with an existing booking (March 10 - March 15, 2025)
        self.room3 = Room.objects.create(
            room_number="103C",
            room_type="Suite",
            rate=100.00,
            room_status="Available",
            capacity=3
        )

        # Creating a guest for the booking
        self.guest = Guest.objects.create(
            guest_id=10001,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890"
        )

        # Creating an existing booking for conflict testing
        self.existing_booking = Booking.objects.create(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )


    def test_create_valid_booking(self):
        """TEST CASE 1: Valid booking creation"""
        booking = Booking(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 6),
            check_out=date(2025, 3, 10),
            payment_status=True,
            total_price=200.00,
        )
        self.assertIsInstance(booking, Booking)
        self.assertIsInstance(booking.room, Room)
        self.assertIsInstance(booking.guest, Guest)

    def test_invalid_dates_check_in_after_check_out(self):
        """TEST CASE 2: Booking with check-in after check-out should fail"""
        booking = Booking(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 6),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()  # Validate before saving

    def test_room_unavailable_during_same_dates(self):
        """TEST CASE 3: Room already booked during the same period"""
        booking = Booking(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 2),
            check_out=date(2025, 3, 4),
            payment_status=True,
            total_price=100.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()
    """
    def test_missing_room(self):
        TEST CASE 4: Booking without a room should fail
        booking = Booking(
            room=None,  # No room specified
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()
    """
    def test_room_unavailable_first_day(self):
        """TEST CASE 5: Room is unavailable on the first day"""
        booking = Booking(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_cross_year_booking(self):
        """TEST CASE 6: Booking that crosses two years"""
        booking = Booking(
            room=self.room1,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 12, 30),
            check_out=date(2026, 1, 2),
            payment_status=True,
            total_price=150.00,
        )
        self.assertIsInstance(booking, Booking)
        self.assertIsInstance(booking.room, Room)
        self.assertIsInstance(booking.guest, Guest)
    """
    def test_guest_id_not_found(self):
        TEST CASE 7: Booking for a guest ID that does not exist
        non_existent_guest = Guest.objects.create(
            guest_id=99999,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone_number="0987654321"
        )

        booking = Booking(
            room=self.room1,
            guest=None,
            booking_status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        booking.full_clean()  # Should not raise an error
        booking.save()
        self.assertEqual(Booking.objects.count(), 2)
    """
    def tearDown(self):
        """Clean up after tests"""
        Booking.objects.all().delete()
        Room.objects.all().delete()
        Guest.objects.all().delete()