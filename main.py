import argparse
import json
import sys
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Student:
    id: int
    name: str
    room: int


@dataclass
class Room:
    id: int
    name: str
    students: list[Student]


class DataLoader(ABC):
    @abstractmethod
    def load(self, file_path: Path) -> list[dict[str, Any]]:
        ...


class JSONDataLoader(DataLoader):
    def load(self, file_path: Path) -> list[dict[str, Any]]:
        try:
            with open(file_path, encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}") from e


class DataExporter(ABC):
    @abstractmethod
    def export(self, rooms: list[Room], output_path: Path) -> None:
        ...


class JSONDataExporter(DataExporter):
    def export(self, rooms: list[Room], output_path: Path) -> None:
        data = []
        for room in rooms:
            room_data = {
                "id": room.id,
                "name": room.name,
                "students": [
                    {"id": student.id, "name": student.name, "room": student.room}
                    for student in room.students
                ],
            }
            data.append(room_data)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class XMLDataExporter(DataExporter):
    def export(self, rooms: list[Room], output_path: Path) -> None:
        root = ET.Element("rooms")

        for room in rooms:
            room_element = ET.SubElement(root, "room")
            room_element.set("id", str(room.id))

            name_element = ET.SubElement(room_element, "name")
            name_element.text = room.name

            students_element = ET.SubElement(room_element, "students")

            for student in room.students:
                student_element = ET.SubElement(students_element, "student")
                student_element.set("id", str(student.id))
                student_element.set("room", str(student.room))
                student_element.text = student.name

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)


class RoomStudentCombiner:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def combine_data(self, students_file: Path, rooms_file: Path) -> list[Room]:
        students_data = self.data_loader.load(students_file)
        rooms_data = self.data_loader.load(rooms_file)

        students = [Student(id=s["id"], name=s["name"], room=s["room"]) for s in students_data]

        students_by_room: dict[int, list[Student]] = {}
        for student in students:
            if student.room not in students_by_room:
                students_by_room[student.room] = []
            students_by_room[student.room].append(student)

        rooms = []
        for room_data in rooms_data:
            room_id = room_data["id"]
            room_students = students_by_room.get(room_id, [])
            room = Room(id=room_id, name=room_data["name"], students=room_students)
            rooms.append(room)

        return rooms


def create_exporter(format_type: str) -> DataExporter:
    format_type = format_type.lower()
    if format_type == "json":
        return JSONDataExporter()
    elif format_type == "xml":
        return XMLDataExporter()
    else:
        raise ValueError(f"Unsupported export format: {format_type}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine students and rooms data and export in specified format."
    )

    parser.add_argument(
        "--students",
        type=Path,
        default=Path("data/students.json"),
        help="Path to students JSON file (default: data/students.json)",
    )

    parser.add_argument(
        "--rooms",
        type=Path,
        default=Path("data/rooms.json"),
        help="Path to rooms JSON file (default: data/rooms.json)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/rooms_output.json"),
        help="Output file path",
    )

    parser.add_argument(
        "--format",
        choices=["json", "xml"],
        default="json",
        help="Output format (default: json)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        data_loader = JSONDataLoader()
        combiner = RoomStudentCombiner(data_loader)
        rooms = combiner.combine_data(args.students, args.rooms)

        exporter = create_exporter(args.format)
        args.output.parent.mkdir(parents=True, exist_ok=True)

        print(f"Exporting {len(rooms)} rooms to {args.output}")
        exporter.export(rooms, args.output)

        print(f"Successfully exported {len(rooms)} rooms to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
