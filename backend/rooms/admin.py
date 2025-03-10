from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_number', 'room_type', 'rate', 'room_status', 'capacity', 'created_date', 'last_changed_date')
    search_fields = ('room_number', 'room_type')
    list_filter = ('room_status', 'room_type')


admin.site.register(Room)

