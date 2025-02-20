def validate_room_capacity(capacity):
    if capacity < 1:
        return {"success": False, "error": "Room capacity must be at least 1."}
    return {"success": True, "message": "Valid room capacity."}


