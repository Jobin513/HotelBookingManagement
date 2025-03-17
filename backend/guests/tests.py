from django.test import TestCase
from django.core.exceptions import ValidationError
from guests.models import Guest


class GuestTest(TestCase):

    def test_valid_guest_entry(self):
        # Test Case 1 - Valid guest entry (valid)
        guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(guest.first_name, "John")
        self.assertEqual(guest.last_name, "Doe")
        self.assertEqual(guest.email, "johndoe@example.com")
        self.assertEqual(guest.phone_number, "2012233210")
        self.assertEqual(guest.address, "123 Main St")
        self.assertEqual(guest.guest_status, "active")


    def test_empty_first_name(self):
        # Test Case 2 - Empty first name (invalid)
        guest = Guest(
            first_name="",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_empty_last_name(self):
        # Test Case 3 - Empty last name (invalid)
        guest = Guest(
            first_name="John",
            last_name="",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_invalid_email_format(self):
        # Test Case 4 - Invalid email format (invalid)
        guest = Guest(
            first_name="John",
            last_name="Doe",
            email="invalidemail.com",  # Missing '@'
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_email_already_exists(self):
        # Test Case 5 - Email already exists (invalid)
        Guest.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        guest2 = Guest(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",  # Duplicate email
            phone_number="2012233210",
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest2.full_clean()

    def test_invalid_phone_number(self):
        # Test Case 6 - Non-numeric phone number (invalid)
        guest = Guest(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="abc123",  # Invalid format
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_phone_number_too_long(self):
        # Test Case 7 - Phone number exceeding 10 digits (invalid)
        guest = Guest(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="201223321012345",  # Too long (15 digits)
            address="123 Main St",
            guest_status="active"
        )
        with self.assertRaises(ValidationError):
            guest.full_clean()

    def test_empty_phone_number(self):
        # Test Case 8 - Empty phone number (valid)
        guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="",  # Should be allowed
            address="123 Main St",
            guest_status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(guest.first_name, "John")
        self.assertEqual(guest.last_name, "Doe")
        self.assertEqual(guest.email, "johndoe@example.com")
        self.assertEqual(guest.phone_number, "")
        self.assertEqual(guest.address, "123 Main St")
        self.assertEqual(guest.guest_status, "active")

    def test_empty_address(self):
        # Test Case 9 - Empty address (valid)
        guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="",  # Should be allowed
            guest_status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(guest.first_name, "John")
        self.assertEqual(guest.last_name, "Doe")
        self.assertEqual(guest.email, "johndoe@example.com")
        self.assertEqual(guest.phone_number, "2012233210")
        self.assertEqual(guest.address, "")
        self.assertEqual(guest.guest_status, "active")
