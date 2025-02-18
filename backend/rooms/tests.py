from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Room


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

    def test_room_capacity_near_low_boundary(self):
        # Test Case 2 - Room capacity just above minimum (valid)
        room2 = Room.objects.create(
            room_number="501A",
            type="Single",
            price=100.00,
            status="Available",
            capacity=1  # Assuming 1 is the minimum valid capacity
        )
        self.assertIsInstance(room2, Room)
        self.assertEqual(room2.capacity, 1)

    def test_room_capacity_low_boundary(self):
        # Test Case 4 - Room capacity at the minimum allowed limit (valid)
        room3 = Room.objects.create(
            room_number="503C",
            type="Single",
            price=120.00,
            status="Available",
            capacity=1  # Minimum valid value
        )
        self.assertIsInstance(room3, Room)
        self.assertEqual(room3.capacity, 1)

    def test_room_capacity_near_high_boundary(self):
        # Test Case 5 - Room capacity just below the maximum (valid)
        room4 = Room.objects.create(
            room_number="504D",
            type="Suite",
            price=500.00,
            status="Available",
            capacity=9  # Assuming 10 is the max allowed capacity
        )
        self.assertIsInstance(room4, Room)
        self.assertEqual(room4.capacity, 9)

    def test_room_capacity_high_boundary(self):
        # Test Case 7 - Room capacity at the maximum allowed limit (valid)
        room5 = Room.objects.create(
            room_number="506F",
            type="Suite",
            price=550.00,
            status="Available",
            capacity=10  # Maximum valid value
        )
        self.assertIsInstance(room5, Room)
        self.assertEqual(room5.capacity, 10)

    def test_room_capacity_non_integer(self):
        # Test Case 1 - Room capacity as a string (invalid)
        room1 = Room(
            room_number="601A",
            type="Single",
            price=100.00,
            status="Available",
            capacity="Four"  # Invalid, should be an integer
        )
        with self.assertRaises(ValidationError):
            room1.full_clean()