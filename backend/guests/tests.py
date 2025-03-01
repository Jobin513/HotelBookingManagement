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
            status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(Guest.objects.count(), 1)

    def test_empty_first_name(self):
        # Test Case 2 - Empty first name (invalid)
        guest = Guest(
            first_name="",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="123 Main St",
            status="active"
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
            status="active"
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
            status="active"
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
            status="active"
        )
        guest2 = Guest(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",  # Duplicate email
            phone_number="2012233210",
            address="123 Main St",
            status="active"
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
            status="active"
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
            status="active"
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
            status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(Guest.objects.count(), 1)

    def test_empty_address(self):
        # Test Case 9 - Empty address (valid)
        guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="2012233210",
            address="",  # Should be allowed
            status="active"
        )
        self.assertIsInstance(guest, Guest)
        self.assertEqual(Guest.objects.count(), 1)