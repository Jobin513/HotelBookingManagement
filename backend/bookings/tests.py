from django.core.exceptions import ValidationError
from django.test import TestCase
from rooms.models import Room
from guests.models import Guest
from bookings.models import Booking


class BookingTest(TestCase):
    def setUp(self):
        # Create a valid room (ID 101)
        self.room = Room.objects.create(
            room_number=101,
            type="Single",
            price=50.00,
            status="Available",
            capacity=2
        )

        # Create a valid guest (ID 10001)
        self.guest = Guest.objects.create(
            guest_id=10001,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890"
        )

    def test_create_valid_booking(self):
        # TEST CASE 1:BOOKING-ADD-VALID (Create a new booking with valid details)
        booking = Booking.objects.create(
            room_id=self.room,
            guest_id=self.guest,
            status="confirmed",
            check_in="2025-03-01",
            check_out="2025-03-05",
            payment_status=True,
            total_price=50.00,
        )
        booking.full_clean()  # This triggers Django's built-in validation
        self.assertIsInstance(booking, Booking)  # Ensure the room object is created correctly
        self.assertEqual(booking.room_id.room_number, 101)  # Check correct room number
        self.assertEqual(booking.guest_id.guest_id, 10001)  # Check correct guest ID


# test case 2:BOOKING-ADD-INVALID-DATES (Create a booking with invalid dates (check_in after check_out))
    def test_invalid_dates_check_in_after_check_out(self):
        booking2 = Booking.objects.create(
            room_id=self.room,
            guest_id=self.guest,
            status="confirmed",
            check_in="2025-10-06",  # Invalid: check_in after check_out
            check_out="2025-10-01",
            payment_status=True,
            total_price=50.00,
        )
        with self.assertRaises(ValidationError):
            booking2.full_clean()

        # test case3 :BOOKING-ADD-ROOM-UNAVAILABLE (booking for a room that is already booked during the same period

    def test_room_unavailable_during_same_dates(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                room_id=self.room,
                guest_id=self.guest,
                status="confirmed",
                check_in="2025-03-01",
                check_out="2025-03-05",
                payment_status=True,
                total_price=50.00,
            )

    # test case 4:BOOKING-ADD-MISSING-ROOM(booking without specifying a room)
    def test_missing_room(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                room_id=None,  # No room specified
                guest_id=self.guest,
                status="confirmed",
                check_in="2025-03-01",
                check_out="2025-03-05",
                payment_status=False,
                total_price=50.00,
            )

    # test case 5:BOOKING-ADD-UNAVAILABLE-FIRST-DAY(booking for a room that is unavailable on the first day but available at the end)
    def test_room_unavailable_first_day(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                room_id=self.room,
                guest_id=self.guest,
                status="cancelled",
                check_in="2025-03-01",  # First day is unavailable
                check_out="2025-03-05",
                payment_status=False,
                total_price=50.00,
            )

    # test case 6:BOOKING-ADD-DEC-TO-JAN (Booking that crosses two years (December to January))
    def test_cross_year_booking(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                room_id=self.room,
                guest_id=self.guest,
                status="cancelled",
                check_in="2025-12-30",
                check_out="2026-01-02",
                payment_status=True,
                total_price=50.00,
            )

    # test case 7:BOOKING-ADD-GUEST-ID-NOT-FOUND(booking for a guest ID that does not exist)
    def test_guest_id_not_found(self):
        with self.assertRaises(Guest.DoesNotExist):
            Booking.objects.create(
                room_id=self.room,
                guest_id=99999,
                status="cancelled",
                check_in="2025-03-01",
                check_out="2025-03-05",
                payment_status=True,
                total_price=50.00,
            )

    def test_booking_in_between_dates(self):
        # TEST CASE 8: BOOKING-INBETWEEN-BOOKED-DATES (Book the available days between two bookings)
        # Create an existing booking for the same room
        Booking.objects.create(
            room_id=self.room,
            guest_id=self.guest,
            status="confirmed",
            check_in="2025-03-06",  # Dates that are available
            check_out="2025-03-08",
            payment_status=True,
            total_price=100.00,
        )

        # Attempt to create a new booking between the existing bookings
        new_booking = Booking.objects.create(
            room_id=self.room,
            guest_id=self.guest,
            status="checked_in",
            check_in="2025-03-01",  # Available dates between 2025-03-01 and 2025-03-05
            check_out="2025-03-05",
            payment_status=True,
            total_price=50.00,
        )

    def tearDown(self):
        # Clean up after tests
        Booking.objects.all().delete()
        Room.objects.all().delete()
        Guest.objects.all().delete()
