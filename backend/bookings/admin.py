from django.contrib import admin

from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'room_id', 'guest_id', 'check_in', 'check_out', 'status', 'payment_status')
    search_fields = ('guest__first_name', 'guest__last_name', 'room__id')
    list_filter = ('status', 'payment_status')
