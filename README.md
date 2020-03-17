# json-to-tables
This is a simple package to help you convert any json schema into SQL-like **csv** tables.

## Installation
Just clone the project or merge the core package into your own project.

## Usage Fast Please
```json_objects = automobiles = [
    {
        "name": "truck",
        "brand": "BMW",
        "num_wheels": 4,
        "engine": {
            "brand": "RR",
            "date_of_production": {
                "day": 3,
                "month": "Feb",
                "year": 1990
            },
            "creators": ["Sandy", "Leslie", "Kane"]
        }
    },
    {
        "name": "bike",
        "num_wheels": 2,
        "top_speed": "100Km/hr",
        "engine": {
            "brand": "Audi",
            "date_of_production": {
                "day": 2,
                "month": "Sep",
                "year": 202
            },
            "creators": ["Anabel", {"GreenMotors": {"CEO": "Charles Green"}}]
        }
    },
]
```
