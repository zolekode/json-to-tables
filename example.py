import json
from core.extent_table import ExtentTable
from core.table_maker import TableMaker

automobiles = [
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

automobiles = json.dumps(automobiles)
automobiles = json.loads(automobiles)

extent_table = ExtentTable()
table_maker = TableMaker(extent_table)
table_maker.convert_json_objects_to_tables(automobiles, "automobiles")
table_maker.show_tables(8)
