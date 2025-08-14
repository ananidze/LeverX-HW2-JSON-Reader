from collections import defaultdict
from pathlib import Path

from .loaders import DataLoader
from .models import Room, Student


class RoomStudentCombiner:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def combine_data(self, students_file: Path, rooms_file: Path) -> list[Room]:
        students_data = self.data_loader.load(students_file)
        rooms_data = self.data_loader.load(rooms_file)

        students = [
            Student(id=s["id"], name=s["name"], room=s["room"]) 
            for s in students_data
        ]

        # Group students by room ID
        students_by_room: dict[int, list[Student]] = defaultdict(list)
        for student in students:
            students_by_room[student.room].append(student)

        # Create Room objects with their associated students
        rooms = []
        for room_data in rooms_data:
            room_id = room_data["id"]
            room_students = students_by_room.get(room_id, [])
            room = Room(id=room_id, name=room_data["name"], students=room_students)
            rooms.append(room)

        return rooms
