from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import format_html
from .forms import RoomAvailabilityForm  # Import the form
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'check_availability_link')  # Display the link

    def check_availability_link(self, obj):
        url = reverse('admin:check_room_availability', args=[obj.id])  # Create a dynamic URL
        return format_html('<a href="{}">Check Availability</a>', url)  # Display as a link

    check_availability_link.short_description = 'Check Availability'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('room/check_availability/<int:room_id>/', self.admin_site.admin_view(self.check_availability), name='check_room_availability'),
        ]
        return custom_urls + urls

    def check_availability(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if request.method == 'POST':
            form = RoomAvailabilityForm(request.POST)
            if form.is_valid():
                check_in = form.cleaned_data['check_in']
                check_out = form.cleaned_data['check_out']
                is_available, error_message = room.is_room_available(check_in, check_out)

                if is_available:
                    message = f"✅ Room {room.room_number} is available from {check_in} to {check_out}."
                else:
                    message = f"❌ Room {room.room_number} is NOT available: {error_message}"

                return render(request, 'admin/check_availability.html', {'form': form, 'room': room, 'message': message})

        else:
            form = RoomAvailabilityForm()

        return render(request, 'admin/check_availability.html', {'form': form, 'room': room})



admin.site.register(Room, RoomAdmin)
