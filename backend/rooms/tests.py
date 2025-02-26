from django.core.exceptions import ValidationError
from django.test import TestCase
from rooms.models import Room



# Room requirements unit testing
class RoomTest(TestCase):

    def test_room_status(self):
        # Test Case 1 - valid room status (Available)
        room1 = Room.objects.create(
            room_number="101A",
            type="Single",
            price=100.00,
            status="Available",
            capacity=2
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.status, "Available")
        # Test Case 2 - invalid room status
        room2 = Room.objects.create(
            room_number="101C",
            type="Single",
            price=100.00,
            status="Unavailable",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()
        # Test Case 3 - empty room status
        room3 = Room.objects.create(
            room_number="101B",
            type="Single",
            price=100.00,
            status="",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()
        # Test Case 4 - valid room status (Booked)
        room4 = Room.objects.create(
            room_number="102A",
            type="Single",
            price=100.00,
            status="Booked",
            capacity=2
        )
        self.assertIsInstance(room4, Room)
        self.assertEqual(room4.status, "Booked")
        # Test Case 5 - valid room status (Under Maintenance)
        room5 = Room.objects.create(
            room_number="102A",
            type="Single",
            price=100.00,
            status="Under Maintenance",
            capacity=2
        )
        self.assertIsInstance(room5, Room)
        self.assertEqual(room5.status, "Under Maintenance")
        # Test Case 6 - non string status
        room6 = Room.objects.create(
            room_number="101B",
            type="Single",
            price=100.00,
            status=5,
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room6.full_clean()

    def test_room_type(self):
        # Test Case 1 - valid room type (Single)
        room1 = Room.objects.create(
            room_number="101A",
            type="Single",
            price=100.00,
            status="Available",
            capacity=2
        )
        room1.full_clean()
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.type, "Single")

        # Test Case 2 - invalid room type (Doble)
        room2 = Room.objects.create(
            room_number="101A",
            type="Doble",
            price=100.00,
            status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

        # Test Case 3- Empty room type
        room3 = Room.objects.create(
            room_number="101A",
            type="",
            price=100.00,
            status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()

        # Test Case 4 - valid room type (Double)
        room4 = Room.objects.create(
            room_number="101A",
            type="Double",
            price=100.00,
            status="Available",
            capacity=2
        )
        self.assertIsInstance(room4, Room)
        self.assertEqual(room4.type, "Double")

        # Test Case 5 - valid room type (Under Maintenance)
        room5 = Room.objects.create(
            room_number="101A",
            type="Suite",
            price=100.00,
            status="Under Maintenance",
            capacity=2
        )
        self.assertIsInstance(room5, Room)
        self.assertEqual(room5.type, "Suite")

        # Test Case 6 - Non string room type
        room6 = Room.objects.create(
            room_number="101A",
            type=5,
            price=100.00,
            status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room6.full_clean()

#test case room near high boundary
    def test_room_price(self):
        """Creates a room with a valid price and checks validity."""

        # Test Case 1 - Room price near high boundary (Valid)
        room = Room.objects.create(
            room_number="301A",
            type="Single",
            price=499.99,  # Near high boundary
            status="Available",
            capacity=2
        )
        room.full_clean()  # This triggers Django's built-in validation
        self.assertIsInstance(room, Room)  # Ensure the room object is created correctly
        self.assertEqual(room.price, 499.99)

        # Test Case 2 - Room price at high boundary (Valid)
        room2 = Room.objects.create(
            room_number="302A",
            type="Double",
            price=500.00,  # High boundary
            status="Available",
            capacity=2
        )
        room2.full_clean()
        self.assertIsInstance(room2, Room)  # Ensure the room object is created correctly
        self.assertEqual(room.price, 500.00)

        # Test Case 3 - Room price exceeding high boundary (Invalid)
        room3 = Room.objects.create(
            room_number="303A",
            type="Suite",
            price=500.01,  # Exceeds high boundary
            status="Available",
            capacity=2
        )
        room3.full_clean()
        self.assertIsInstance(room3, Room)
        self.assertEqual(room3.price, 500.01)

        # Test Case 4 - Room price below low boundary (Invalid)
        room4 = Room.objects.create(
            room_number="304A",
            type="Single",
            price=49.99,  # Below valid range
            status="Available",
            capacity=2
        )
        with self.assertRaises(ValidationError):
            room4.full_clean()

        # Test case 5 - for empty room price
        def test_room_price_empty(self):
            """Creates a room with an empty price and expects a validation error."""
            room = Room(
                room_number="305A",
                type="Single",
                price=None,  # Empty price
                status="Available",
                capacity=2
            )
            with self.assertRaises(ValidationError):
                room.full_clean()

        # Test case 6 - for non-decimal room price
        def test_room_price_non_decimal(self):
            """Creates a room with a non-decimal price and expects a validation error."""
            room = Room(
                room_number="306A",
                type="Single",
                price="one hundred",  # Non-decimal value
                status="Available",
                capacity=2
            )
            with self.assertRaises(ValidationError):
                room.full_clean()

    def test_room_capacity_near_low_boundary(self):
        # Test Case 1 - Room capacity just above minimum (valid)
        room1 = Room.objects.create(
            room_number="101A",
            type="Single",
            price=50.00,
            status="Available",
            capacity=1
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.capacity, 1)

        # Test Case 2 -  Room capacity lower than allowable room capacity (invalid)
        room2 = Room(
            room_number="102B",
            type="Double",
            price=100.00,
            status="Available",
            capacity=0  # Assuming 1 is the minimum valid capacity
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

    def test_room_capacity_high_boundary(self):
        # Test Case 3 - Room capacity at the maximum (valid)
        room1 = Room.objects.create(
            room_number="103D",
            type="Suite",
            price=200.00,
            status="Available",
            capacity=5  #  it has max capacity is 5
        )
        self.assertIsInstance(room1, Room)
        self.assertEqual(room1.capacity, 5)

    # Test Case 4 - Room capacity just above maximum (invalid)
    def test_room_capacity_near_high_boundary(self):
        room3 = Room(
            room_number="104E",
            type="Suite",
            price=200.00,
            status="Available",
            capacity=6
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

    def test_room_capacity_non_integer(self):
        # Test Case 6 - Room capacity as a string (invalid)
        room1 = Room(
            room_number="201A",
            type="Single",
            price=50.00,
            status="Available",
            capacity="Four"  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room1.full_clean()  # Ensure validation runs before saving

        # Test Case 7 - Room capacity as a float (invalid)
        room2 = Room(
            room_number="202B",
            type="Double",
            price=100.00,
            status="Available",
            capacity=2.5 # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room2.full_clean()

        # Test Case 8 - Room capacity as a boolean (invalid)
        room3 = Room(
            room_number="203C",
            type="Suite",
            price=200.00,
            status="Available",
            capacity=True  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room3.full_clean()

        # Test Case 9 - Room capacity as None (invalid)
        room4 = Room(
            room_number="204D",
            type="Suite",
            price=200.00,
            status="Available",
            capacity=None  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room4.full_clean()

    def test_room_capacity_invalid(self):
        # Test Case 10 - Negative capacity (invalid)
        room = Room(
            room_number="205E",
            type="Double",
            price=150.00,
            status="Available",
            capacity=-1  # Invalid negative capacity
        )
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_room_capacity_valid(self):
        # Test Case 11 - Valid capacity within range
        room = Room.objects.create(
            room_number="206F",
            type="Suite",
            price=200.00,
            status="Available",
            capacity=3  # A valid value within allowable range (1-5)
        )
        self.assertIsInstance(room, Room)
        self.assertEqual(room.capacity, 3)
