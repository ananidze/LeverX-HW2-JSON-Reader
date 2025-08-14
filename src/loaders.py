import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


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
