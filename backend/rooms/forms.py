# rooms/forms.py

from django import forms
from datetime import datetime


class RoomAvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Check-In Date"
    )
    check_out = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Check-Out Date"
    )

    def check_availability(self, room):
        check_in = self.cleaned_data['check_in']
        check_out = self.cleaned_data['check_out']
        return room.is_room_available(check_in, check_out)
