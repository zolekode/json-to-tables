# json-to-tables
This is a simple package to help you convert any dynamic json file into SQL-like **csv** tables.

## Installation
Just clone the project or merge the core package into your own project.

## Usage
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

```

Here are the result obtained after running the script.

```
SHOWING TABLES :D


automobiles
   ID   name brand num_wheels engine top_speed
0   0  truck   BMW          4      0      None
1   1   bike  None          2      1  100Km/hr
2   2   None  None       None   None      None
____________________________________________________

```

Note: The truck has no top_speed attribute, so its value is None. The engine attribute contains reference keys to the engine table. Note that For the the bike, the engine reference key is 1. Looking at the table engine, you notive that ID=1 has the brand=Audi. Which was the engine brand for the bike in the JSON file.

```

engine
   ID brand date_of_production
0   0    RR                  0
1   1  Audi                  1
2   2  None               None
____________________________________________________

```

Note: The same thing goes for the date_of_production of the engine. Where the ID=0, the brand=RR and the date_of_production=0. This 0 is the reference key to the table date_of_production. Again looking at the date of production table where the ID=0 you notice that the month=Feb which is the exact month for the BMW in the original JSON file.

```

date_of_production
   ID   day month  year
0   0     3   Feb  1990
1   1     2   Sep   202
2   2  None  None  None
____________________________________________________


engine_?_creators
  ID PARENT_ID is_scalar  scalar complex
0  0         0      True   Sandy    None
1  1         0      True  Leslie    None
2  2         0      True    Kane    None
3  3         1      True  Anabel    None
4  4         1     False    None       0
____________________________________________________

```

Note: For Multivalued attributes (like lists) it is a little trickier. There are 4 attributes you need to consider.
* The parent ID: The table engine_?_creators was generated from the creators attribute contained in the engine attribute found in the JSON file. Hence the name engine_?_creators. The ? mark character tells you creators was a list in engine object.
Therefore, the where the PARENT_ID=0, this just means, refer to the row with ID=0 in the engine table. 

Let us test this. Look at the attribute scalar with values Sandy, Leslie and Kane. They all have a parent ID=0. This exactly corresponds to the engine with brand=RR.

* The is_scalar attribute: The value of this column is set to `True` if the value found in the list is a scalar. Note that there was only one case where the value wasn't a scalar i.e `{"GreenMotors": {"CEO": "Charles Green"}}`.

* The scalar attribute: The value is equal to the value found in the list if is_scalar=True. Else the value=None. Again there is only one case where this happens.

* The complex attribute: If a list contains a non-scalar value like `{"GreenMotors": {"CEO": "Charles Green"}}`, a new table is created for that value and an id is set to reference to that object. For scalar values, the cell value is set to `None`.
In the above example, the row with ID=4 has complex=0. This means you should look for ...

```

GreenMotors
   ID            CEO
0   0  Charles Green
1   1           None
____________________________________________________


engine_?_creators_$_GreenMotors
   ID GreenMotors
0   0           0
1   1        None
```
