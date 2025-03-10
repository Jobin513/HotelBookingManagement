from django.db import models
from django.core.exceptions import ValidationError
from bookings.models import Booking


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
    ]

    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def clean(self):
        if not self.booking:
            raise ValidationError("Booking cannot be empty or invalid.")

        if self.amount == "":
            raise ValidationError("Amount cannot be empty.")

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if self.amount > 10000:
            raise ValidationError("Amount cannot exceed 10,000.")

        if self.payment_method not in dict(self.PAYMENT_METHOD_CHOICES):
            raise ValidationError(f"Invalid payment method: {self.payment_method}")

        super().clean()

    def _str_(self):
        return f"Payment {self.payment_id} - {self.booking} - {self.amount} {self.payment_method}"