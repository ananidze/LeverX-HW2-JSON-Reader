
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from .models import Room


class ExportFormat(Enum):
    """Supported export formats."""
    JSON = "json"
    XML = "xml"


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


def create_exporter(format_type: str) -> DataExporter:
    exporters: dict[str, type[DataExporter]] = {
        ExportFormat.JSON.value: JSONDataExporter,
        ExportFormat.XML.value: XMLDataExporter,
    }

    try:
        return exporters[format_type.lower()]()
    except KeyError as err:
        raise ValueError(
            f"Unsupported export format: {format_type}. Supported formats: "
            f"{', '.join(exporters.keys())}"
        ) from err
    
    