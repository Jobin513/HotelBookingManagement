from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'type', 'price', 'status', 'capacity', 'created_date', 'last_changed_date')
    search_fields = ('room_number', 'type')
    list_filter = ('status', 'type')


admin.site.register(Room)

