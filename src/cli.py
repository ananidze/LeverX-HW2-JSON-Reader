
import argparse
import sys
from pathlib import Path

from .combiners import RoomStudentCombiner
from .exporters import create_exporter
from .loaders import JSONDataLoader


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


def main() -> None:
    args = parse_arguments()

    try:
        data_loader = JSONDataLoader()
        combiner = RoomStudentCombiner(data_loader)
        
        rooms = combiner.combine_data(args.students, args.rooms)

        # Create output directory if it doesn't exist
        args.output.parent.mkdir(parents=True, exist_ok=True)

        exporter = create_exporter(args.format)
        print(f"Exporting {len(rooms)} rooms to {args.output}")
        exporter.export(rooms, args.output)

        print(f"Successfully exported {len(rooms)} rooms to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
