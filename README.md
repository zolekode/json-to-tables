# json-to-tables
This is a simple package to help you convert any dynamic json file into SQL-like **csv** tables.

## Installation
Just clone the project or merge the core package into your own project.

## Usage Fast Please
Assume you want to convert the JSON file below to tables.
```automobiles = [
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
First, you load the JSON string.
```
# automobiles = json.dumps(automobiles) uncomment this line if you directly copy the JSON file above in your script for testing
```
```automobiles = json.loads(automobiles)```

Then run the following code:
```
# Creates an extent table object that manages all the tables
extent_table = ExtentTable()


# Pass the extent table object to the table maker
table_maker = TableMaker(extent_table) 


# Below is the name of the objects you are trying to convert. In our case, we are dealing with automobiles hence the "root" name will be automobiles
root_table_name = "automobiles" 


table_maker.convert_json_objects_to_tables(automobiles, root_table_name)


# num_elements is the max number of elements to show when printing the tables
table_maker.show_tables(num_elements=5)
