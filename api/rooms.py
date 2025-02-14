#view room
@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
#view room
@api_view(['PUT'])
def update_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RoomSerializer(room, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#update room
#PATCH - Partial Update Room
#This endpoint allows updating specific fields of a room (e.g., changing only the status).
@api_view(['PATCH'])
def partial_update_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RoomSerializer(room, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)