from dataclasses import dataclass


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
