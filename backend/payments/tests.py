from datetime import date

from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from payments.models import Payment
from bookings.models import Booking
from guests.models import Guest
from rooms.models import Room


class PaymentModelTest(TestCase):

    def setUp(self):
        """Set up test data for Payment tests"""

        # Create a room for the test
        self.room = Room.objects.create(
            room_number="101A",
            room_type="Single",
            rate=50.00,
            room_status="Available",
            capacity=2
        )

        # Create a guest for the test with the correct field name 'guest_status'
        self.guest = Guest.objects.create(
            guest_id=10001,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            address="123 main street",
            guest_status="active"
        )

        # Create a booking for the test
        self.booking = Booking.objects.create(
            room=self.room,
            guest=self.guest,
            booking_status="confirmed",
            check_in=date(2025, 3, 1),
            check_out=date(2025, 3, 5),
            payment_status=True,
            total_price=50.00
        )

    def test_valid_payment(self):
        """Test Case 1 - Valid Payment (Valid)"""
        payment = Payment.objects.create(
            booking=self.booking,
            amount=50.00,
            payment_method="Credit Card"
        )
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.booking.booking_id, self.booking.booking_id)
        self.assertEqual(payment.amount, 50.00)
        self.assertEqual(payment.payment_method, "Credit Card")

    def test_empty_amount(self):
        """Test Case 2 - Empty Amount (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount="",
            payment_method="Debit Card"
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_negative_amount(self):
        """Test Case 3 - Negative Amount (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount=-10.00,
            payment_method="Credit Card"
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_zero_amount(self):
        """Test Case 4 - Zero Amount (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount=0.00,
            payment_method="Credit Card"
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_minimum_amount(self):
        """Test Case 5 - Minimum Payment Amount (Valid)"""
        payment = Payment.objects.create(
            booking=self.booking,
            amount=0.01,
            payment_method="Debit Card"
        )
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.booking.booking_id, self.booking.booking_id)
        self.assertEqual(payment.amount, 0.01)
        self.assertEqual(payment.payment_method, "Debit Card")

    def test_maximum_amount(self):
        """Test Case 6 - Maximum Payment Amount (Valid)"""
        payment = Payment.objects.create(
            booking=self.booking,
            amount=10000.00,  # Assuming 10,000 is the max allowed
            payment_method="Credit Card"
        )
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.booking.booking_id, self.booking.booking_id)
        self.assertEqual(payment.amount, 10000.00)
        self.assertEqual(payment.payment_method, "Credit Card")

    def test_exceeding_maximum(self):
        """Test Case 7 - Exceeding Maximum Payment Amount (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount=10000.01,  # Just above the max
            payment_method="Credit Card"
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_unsupported_payment_method(self):
        """Test Case 8 - Unsupported Payment Method (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount=100.00,
            payment_method="Bitcoin"  # Not in ENUM
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_invalid_booking(self):
        """Test Case 9 - Invalid Booking (Invalid)"""
        payment = Payment(
            booking=None,
            amount=50.00,
            payment_method="Credit Card"
        )
        with self.assertRaises(IntegrityError):
            payment.save()

    def test_empty_booking(self):
        """Test Case 10 - Empty Booking (Invalid)"""
        payment = Payment(
            booking=None,
            amount=50.00,
            payment_method="Credit Card"
        )
        with self.assertRaises(IntegrityError):
            payment.save()

    def test_empty_payment_method(self):
        """Test Case 11 - Empty Payment Method (Invalid)"""
        payment = Payment(
            booking=self.booking,
            amount=50.00,
            payment_method=""  # Empty payment method
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_payment_with_3_decimal_points(self):
        """Test Case 12 - Payment with 3 Decimal Points (Valid)"""
        payment = Payment.objects.create(
            booking=self.booking,
            amount=50.005,  # 3 decimal points
            payment_method="Credit Card"
        )
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.booking.booking_id, self.booking.booking_id)
        self.assertEqual(payment.amount, 50.005)
        self.assertEqual(payment.payment_method, "Credit Card")