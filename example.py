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
            "compatible": True,
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
            "compatible": False,
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

# Set cast_none_to_nan to True if you prefer real Null values (recommended)
# Set cast_object_to_bool to True if you want to save real json booleans (recommended but slower)
# table_maker.save_tables("./", cast_none_to_nan=True, cast_object_to_bool=True)

# Saving the state of the ExtentTable object for later use

extent_table.save_extent_table_state()

extent_table = ExtentTable()

table_maker = TableMaker(extent_table)

extent_table.load_extent_table_state()

# Continue adding objects. We are basically just saving the info twice for the sake of example.

table_maker.convert_json_objects_to_tables(automobiles, "automobiles")

table_maker.show_tables(8)
