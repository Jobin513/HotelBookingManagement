from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import Room
from .serializers import RoomSerializer


class RoomList(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

class RoomAvailability(APIView):
    def get(self, request, room_id):
        # Get the room based on room_id
        room = get_object_or_404(Room, id=room_id)

        # Get the user-inputted check-in and check-out dates from request (assuming they're sent via GET)
        check_in = request.GET.get('check_in')  # For example: "2025-05-01T15:00"
        check_out = request.GET.get('check_out')  # For example: "2025-05-05T11:00"

        if not check_in or not check_out:
            return JsonResponse({"error": "Both check_in and check_out dates are required."}, status=400)

        try:
            # Convert the string dates to datetime objects
            check_in = datetime.fromisoformat(check_in)
            check_out = datetime.fromisoformat(check_out)
        except ValueError:
            return JsonResponse({"error": "Invalid date format."}, status=400)

        # Check if room is available
        is_available, error_message = room.is_room_available(check_in, check_out)

        if is_available:
            return JsonResponse({"message": "Room is available!"}, status=200)
        else:
            return JsonResponse({"error": error_message}, status=400)
