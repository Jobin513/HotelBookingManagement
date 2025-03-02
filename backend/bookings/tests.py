from django.core.exceptions import ValidationError
from django.test import TestCase
from bookings.models import Booking
from rooms.models import Room
from guests.models import Guest
from datetime import date


class BookingTest(TestCase):

    def setUp(self):
        """Set up test data for Booking tests"""
        # Creating a room for the test
        self.room = Room.objects.create(
            room_number=101,
            type="Single",
            price=50.00,
            status="Available",
            capacity=2
        )

        # Creating a guest for the test
        self.guest = Guest.objects.create(
            guest_id=10001,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890"
        )

        # Creating an existing booking for conflict testing
        self.existing_booking = Booking.objects.create(
            room=self.room,
            guest=self.guest,
            status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )

    def test_create_valid_booking(self):
        """TEST CASE 1: Valid booking creation"""
        booking = Booking(
            room=self.room,
            guest=self.guest,
            status="confirmed",
            check_in=date(2025, 3, 6),
            check_out=date(2025, 3, 10),
            payment_status=True,
            total_price=200.00,
        )
        booking.full_clean()  # Validate before saving
        booking.save()
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(booking.room.room_number, 101)
        self.assertEqual(booking.guest.guest_id, 10001)

    def test_invalid_dates_check_in_after_check_out(self):
        """TEST CASE 2: Booking with check-in after check-out should fail"""
        booking = Booking(
            room=self.room,
            guest=self.guest,
            status="confirmed",
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
            room=self.room,
            guest=self.guest,
            status="confirmed",
            check_in=date(2025, 3, 2),
            check_out=date(2025, 3, 4),
            payment_status=True,
            total_price=100.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_missing_room(self):
        """TEST CASE 4: Booking without a room should fail"""
        booking = Booking(
            room=None,  # No room specified
            guest=self.guest,
            status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_room_unavailable_first_day(self):
        """TEST CASE 5: Room is unavailable on the first day"""
        booking = Booking(
            room=self.room,
            guest=self.guest,
            status="confirmed",
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
            room=self.room,
            guest=self.guest,
            status="confirmed",
            check_in=date(2025, 12, 30),
            check_out=date(2026, 1, 2),
            payment_status=True,
            total_price=150.00,
        )
        booking.full_clean()  # Should not raise an error
        booking.save()
        self.assertEqual(Booking.objects.count(), 2)

    def test_guest_id_not_found(self):
        """TEST CASE 7: Booking for a guest ID that does not exist"""
        non_existent_guest = Guest.objects.create(
            guest_id=99999,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="0987654321"
        )

        booking = Booking(
            room=self.room,
            guest=non_existent_guest,
            status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00,
        )
        booking.full_clean()  # Should not raise an error
        booking.save()
        self.assertEqual(Booking.objects.count(), 2)

    def tearDown(self):
        """Clean up after tests"""
        Booking.objects.all().delete()
        Room.objects.all().delete()
        Guest.objects.all().delete()