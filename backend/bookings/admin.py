from django.contrib import admin

from bookings.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'room', 'guest', 'check_in', 'check_out')


admin.site.register(Booking, BookingAdmin)
