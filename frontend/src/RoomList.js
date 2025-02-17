import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RoomList() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/rooms/')
      .then(response => {
        setRooms(response.data);
      })
      .catch(error => {
        console.error('Error fetching rooms:', error);
      });
  }, []);

  return (
    <div>
      <h1>Room List</h1>
      <ul>
        {rooms.map(room => (
          <li key={room.id}>
            {room.room_number} - {room.type} - ${room.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RoomList;