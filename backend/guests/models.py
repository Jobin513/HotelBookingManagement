from typing import re

from django.db import models
from pydantic_core import ValidationError


class Guest(models.Model):
    class Meta:
        app_label = 'guests'
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    guest_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def clean(self):
        if not self.first_name:
            raise ValidationError("First name cannot be empty.")
        if not self.last_name:
            raise ValidationError("Last name cannot be empty.")
        if not self.email:
            raise ValidationError("Email cannot be empty.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email format.")
        if Guest.objects.filter(email=self.email).exists():
            raise ValidationError("Email already exists.")

        # Phone number validation
        if not self.phone_number.isdigit():
            raise ValidationError("Phone number must be numeric.")
        if len(self.phone_number) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")

        # Address validation
        if not self.address:
            raise ValidationError("Address cannot be empty.")

        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError("Invalid status. Must be Active or Inactive.")
        super().clean()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.status})"

