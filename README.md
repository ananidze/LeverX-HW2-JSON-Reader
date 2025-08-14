# JSON Reader - Room and Student Data Combiner

A Python script that combines student and room data from JSON files and exports the results.

## Task Description

You are given two files:
- `students.json`
- `rooms.json`

This script:
- Loads data from both files
- Combines the data into a list of rooms, where each room includes the students assigned to it
- Exports the resulting structure in the specified format: JSON or XML
- Accepts input parameters via the command line (CLI)

## Usage

```bash
python main.py --students data/students.json --rooms data/rooms.json --format json --output output/
```

## Output Formats

- **JSON**: Combined room and student data in JSON format
- **XML**: Combined room and student data in XML format