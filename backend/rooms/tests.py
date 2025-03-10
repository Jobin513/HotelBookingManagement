from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from rooms.models import Room
from bookings.models import Booking
from guests.models import Guest


# Room requirements unit testing
class RoomTest(TestCase):

    def test_room_status(self):
        # Test Case 1 - valid room status (Available)
        """
        Identifier: VALID-ROOM-CREATION
        Test Case: Create a new room with valid parameters
        Preconditions: Room number 101A must not exist in the database.
        Input Values: room_number: 101A,  type: single rate: 100.00 capacity: 2, status: Available
        Execution Steps: Navigate to add room page. Input room_number, floor_number, type, status, price, capacity for the room details. Click add room.
        Output Values: N/A
        Postconditions: Program displays a message “Room 101 has successfully been added.” Program creates a database entry for the newly added room. Program can now search for room 101 with the correct details.
        """
        room1 = Room.objects.create(
            room_number="101A",
            room_type="Single",
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.room_status, "Available")
        # Test Case 2 - invalid room status
        """
        Identifier: INVALID-ROOM-STATUS
        Test Case: Attempt to create a room with an invalid status
        Preconditions: Room number 101 must not exist in the database.
        Input Values:
        room_number: 101C,  room_type: single, rate: 100.00, capacity: 2, room_status: unavailable
        Execution Steps:
        Navigate to the "Add Room" page.
        Input room_number, room_type, rate, capacity, room_status
        Click "Add Room."
        Output Values: 
        Postconditions: Error message: "Invalid room status. Must be “available”, “booked", "Under Maintenance.”. Program exits. No room entry is created.
        """
        room2 = Room.objects.create(
            room_number="101C",
            room_type="Single",
            rate=100.00,
            room_status="Unavailable",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()
        # Test Case 3 - empty room status
        room3 = Room.objects.create(
            room_number="101B",
            room_type="Single",
            rate=100.00,
            room_status="",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()
        # Test Case 4 - valid room status (Booked)
        room4 = Room.objects.create(
            room_number="102A",
            room_type="Single",
            rate=100.00,
            room_status="Booked",
            capacity=2
        )
        self.assertIsInstance(room4, Room)
        self.assertEqual(room4.room_status, "Booked")
        # Test Case 5 - valid room status (Under Maintenance)
        room5 = Room.objects.create(
            room_number="102B",
            room_type="Single",
            rate=100.00,
            room_status="Under Maintenance",
            capacity=2
        )
        self.assertIsInstance(room5, Room)
        self.assertEqual(room5.room_status, "Under Maintenance")
        # Test Case 6 - non string status
        room6 = Room.objects.create(
            room_number="103B",
            room_type="Single",
            rate=100.00,
            room_status=5,
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room6.full_clean()

    def test_room_type(self):
        # Test Case 1 - valid room type (Single)
        room1 = Room.objects.create(
            room_number="103A",
            room_type="Single",
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        room1.full_clean()
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.room_type, "Single")

        # Test Case 2 - invalid room type (Doble)
        room2 = Room.objects.create(
            room_number="104A",
            room_type="Doble",
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

        # Test Case 3- Empty room type
        room3 = Room.objects.create(
            room_number="105A",
            room_type="",
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()

        # Test Case 4 - valid room type (Double)
        room4 = Room.objects.create(
            room_number="106A",
            room_type="Double",
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        self.assertIsInstance(room4, Room)
        self.assertEqual(room4.room_type, "Double")

        # Test Case 5 - valid room type (Under Maintenance)
        room5 = Room.objects.create(
            room_number="107A",
            room_type="Suite",
            rate=100.00,
            room_status="Under Maintenance",
            capacity=2
        )
        self.assertIsInstance(room5, Room)
        self.assertEqual(room5.room_type, "Suite")

        # Test Case 6 - Non string room type
        room6 = Room.objects.create(
            room_number="108A",
            room_type=5,
            rate=100.00,
            room_status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room6.full_clean()

#test case room near high boundary
    def test_room_price(self):
        """Creates a room with a valid rate and checks validity."""

        # Test Case 1 - Room rate near high boundary (Valid)
        room = Room.objects.create(
            room_number="301A",
            room_type="Single",
            rate=499.99,  # Near high boundary
            room_status="Available",
            capacity=2
        )
        self.assertIsInstance(room, Room)  # Ensure the room object is created correctly
        self.assertEqual(room.rate, 499.99)

        # Test Case 2 - Room rate at high boundary (Valid)
        room2 = Room.objects.create(
            room_number="302A",
            room_type="Double",
            rate=500.00,  # High boundary
            room_status="Available",
            capacity=2
        )
        room2.full_clean()
        self.assertIsInstance(room2, Room)  # Ensure the room object is created correctly
        self.assertEqual(room2.rate, 500.00)

        # Test Case 3 - Room rate exceeding high boundary (Invalid)
        room3 = Room.objects.create(
            room_number="303A",
            room_type="Suite",
            rate=500.01,  # Exceeds high boundary
            room_status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()

        # Test Case 4 - Room rate below low boundary (Invalid)
        room4 = Room.objects.create(
            room_number="304A",
            room_type="Single",
            rate=49.99,  # Below valid range
            room_status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room4.full_clean()

        # Test case 5 - for empty room rate
        def test_room_price_empty(self):
            """Creates a room with an empty rate and expects a validation error."""
            room = Room(
                room_number="305A",
                room_type="Single",
                rate=None,  # Empty rate
                room_status="Available",
                capacity=2
            )
            with self.assertRaises(ValidationError):
                room.full_clean()

        # Test case 6 - for non-decimal room rate
        def test_room_price_non_decimal(self):
            """Creates a room with a non-decimal rate and expects a validation error."""
            room = Room(
                room_number="306A",
                room_type="Single",
                rate="one hundred",  # Non-decimal value
                room_status="Available",
                capacity=2
            )
            with self.assertRaises(ValidationError):
                room.full_clean()

    def test_room_capacity_near_low_boundary(self):
        # Test Case 1 - Room capacity just above minimum (valid)
        room1 = Room.objects.create(
            room_number="109A",
            room_type="Single",
            rate=50.00,
            room_status="Available",
            capacity=1
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.capacity, 1)

        # Test Case 2 -  Room capacity lower than allowable room capacity (invalid)
        room2 = Room(
            room_number="104B",
            room_type="Double",
            rate=100.00,
            room_status="Available",
            capacity=0  # Assuming 1 is the minimum valid capacity
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

    def test_room_capacity_high_boundary(self):
        # Test Case 3 - Room capacity at the maximum (valid)
        room1 = Room.objects.create(
            room_number="103D",
            room_type="Suite",
            rate=200.00,
            room_status="Available",
            capacity=5  #  it has max capacity is 5
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.capacity, 5)

    # Test Case 4 - Room capacity just above maximum (invalid)
    def test_room_capacity_near_high_boundary(self):
        room3 = Room(
            room_number="104E",
            room_type="Suite",
            rate=200.00,
            room_status="Available",
            capacity=6
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()

    def test_room_capacity_non_integer(self):
        # Test Case 6 - Room capacity as a string (invalid)
        room1 = Room(
            room_number="201A",
            room_type="Single",
            rate=50.00,
            room_status="Available",
            capacity="Four"  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room1.full_clean()  # Ensure validation runs before saving

        # Test Case 7 - Room capacity as a float (invalid)
        """room2 = Room(
            room_number="202B",
            room_type="Double",
            rate=100.00,
            room_status="Available",
            capacity=2.5  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()
        
        # Test Case 8 - Room capacity as a boolean (invalid)
        room3 = Room(
            room_number="203C",
            room_type="Suite",
            rate=200.00,
            room_status="Available",
            capacity=True  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()
        """
        # Test Case 9 - Room capacity as None (invalid)
        room4 = Room(
            room_number="204D",
            room_type="Suite",
            rate=200.00,
            room_status="Available",
            capacity=None  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room4.full_clean()

    def test_room_capacity_invalid(self):
        # Test Case 10 - Negative capacity (invalid)
        room = Room(
            room_number="205E",
            room_type="Double",
            rate=150.00,
            room_status="Available",
            capacity=-1  # Invalid negative capacity
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_room_capacity_valid(self):
        # Test Case 11 - Valid capacity within range
        room = Room.objects.create(
            room_number="206F",
            room_type="Suite",
            rate=200.00,
            room_status="Available",
            capacity=3  # A valid value within allowable range (1-5)
        )
        self.assertIsInstance(room, Room)
        self.assertEqual(room.capacity, 3)

    def setUp(self):
        """Set up test data for Is_Room_Available tests"""

        # Create rooms
        self.room1 = Room.objects.create(
            room_number="101D",
            room_type="Single",
            rate=50.00,
            room_status="Maintenance",
            capacity=2
        )

        self.room2 = Room.objects.create(
            room_number="102C",
            room_type="Double",
            rate=75.00,
            room_status="Available",
            capacity=4
        )

        self.room3 = Room.objects.create(
            room_number="103C",
            room_type="Suite",
            rate=100.00,
            room_status="Available",
            capacity=3
        )

        # Create guest for booking
        self.guest = Guest.objects.create(
            guest_id=10001,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890"
        )

        # Create existing booking for conflict testing
        self.existing_booking = Booking.objects.create(
            room=self.room3,
            guest=self.guest,
            booking_status="confirmed",
            check_in=datetime(2025, 3, 10),
            check_out=datetime(2025, 3, 15),
            payment_status=True,
            total_price=50.00,
        )

    def test_room_available_no_bookings(self):
        """Test booking a room with no prior bookings"""
        check_in = datetime(2028, 3, 5)
        check_out = datetime(2028, 3, 7)
        self.assertTrue(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_room_unavailable_due_to_full_overlap(self):
        """Test room with full overlap of existing booking"""
        check_in = datetime(2025, 3, 10)
        check_out = datetime(2025, 3, 15)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_room_unavailable_partial_overlap_start(self):
        """Test room with partial overlap at the start"""
        check_in = datetime(2025, 3, 8)
        check_out = datetime(2025, 3, 12)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_room_unavailable_partial_overlap_end(self):
        """Test room with partial overlap at the end"""
        check_in = datetime(2025, 3, 13)
        check_out = datetime(2025, 3, 18)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_booking_completely_encompassing_existing_booking(self):
        """Test booking completely covers an existing one"""
        check_in = datetime(2025, 3, 5)
        check_out = datetime(2025, 3, 20)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_exact_match_with_existing_booking(self):
        """Test booking dates exactly match an existing booking"""
        check_in = datetime(2025, 3, 10)
        check_out = datetime(2025, 3, 15)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_room_unavailable_end_date_matches_existing_start(self):
        """Test booking with end date matching an existing booking's start date"""
        check_in = datetime(2025, 3, 10)
        check_out = datetime(2025, 3, 16)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))
    """
    def test_room_unavailable_start_date_matches_existing_end(self):
        Test booking with start date matching an existing booking's end date
        check_in = datetime(2025, 3, 15)
        check_out = datetime(2025, 3, 20)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))
    """
    def test_single_day_booking(self):
        """Test booking for a single day"""
        check_in = datetime(2027, 3, 6)
        check_out = datetime(2027, 3, 7)
        self.assertTrue(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_invalid_date_range(self):
        """Test when the start date is after the end date"""
        check_in = datetime(2025, 3, 7)
        check_out = datetime(2025, 3, 5)
        self.assertFalse(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_room_under_maintenance(self):
        """Test booking a room under maintenance"""
        check_in = datetime(2025, 3, 10)
        check_out = datetime(2025, 3, 15)
        self.assertFalse(self.room1.is_room_available(check_in, check_out, self.room1.id))

    """
    def test_empty_room_id(self):
        Test booking with an empty room ID
        check_in = datetime(2025, 3, 10)
        check_out = datetime(2025, 3, 15)
        self.assertFalse(Room.is_room_available(check_in, check_out, None))
    """
    def test_empty_check_in(self):
        """Test booking with an empty check-in date"""
        check_out = datetime(2025, 3, 15)
        self.assertFalse(self.room3.is_room_available(None, check_out, self.room3.id))

    def test_empty_check_out(self):
        """Test booking with an empty check-out date"""
        check_in = datetime(2025, 3, 10)
        self.assertFalse(self.room3.is_room_available(check_in, None, self.room3.id))

    def test_non_date_check_in_value(self):
        """Test booking with a non-date check-in value"""
        check_in = "invalid_date"
        check_out = datetime(2025, 3, 15)
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_non_date_check_out_value(self):
        """Test booking with a non-date check-out value"""
        check_in = datetime(2025, 3, 10)
        check_out = "invalid_date"
        self.assertFalse(self.room3.is_room_available(check_in, check_out, self.room3.id))

    def test_past_check_in_date(self):
        """Test booking with a past check-in date"""
        check_in = datetime(2024, 3, 5)
        check_out = datetime(2024, 3, 7)
        self.assertFalse(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_past_check_out_date(self):
        """Test booking with a past check-out date"""
        check_in = datetime(2024, 3, 5)
        check_out = datetime(2024, 3, 10)
        self.assertFalse(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_max_duration_exceeded(self):
        """Test booking when max duration is exceeded (14 days)"""
        check_in = datetime(2025, 3, 1)
        check_out = datetime(2025, 3, 20)
        self.assertFalse(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_min_duration_booking(self):
        """Test booking with the minimum duration (2 days)"""
        check_in = datetime(2025, 5, 5)
        check_out = datetime(2025, 5, 7)
        self.assertTrue(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_max_boundary_duration(self):
        """Test booking with the max boundary duration (15 days)"""
        check_in = datetime(2025, 3, 1)
        check_out = datetime(2025, 3, 16)
        self.assertFalse(self.room2.is_room_available(check_in, check_out, self.room2.id))

    def test_min_boundary_duration(self):
        """Test booking with the min boundary duration (1 day)"""
        check_in = datetime(2026, 3, 5)
        check_out = datetime(2026, 3, 6)
        self.assertTrue(self.room2.is_room_available(check_in, check_out, self.room2.id))
