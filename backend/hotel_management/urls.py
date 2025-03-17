from django.contrib import admin
from django.urls import path, include

from bookings.views import BookingList
from guests.views import GuestList
from rooms.views import RoomList, RoomAvailability  # Import RoomAvailability

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rooms/', RoomList.as_view(), name='room-list'),
    path('api/rooms/<int:room_id>/availability/', RoomAvailability.as_view(), name='room-availability'),
    path('api/bookings/', BookingList.as_view(), name='booking-list'),
    path('api/guests/', GuestList.as_view(), name='guest-list'),
    path('payments/', include('payments.urls')),
]
