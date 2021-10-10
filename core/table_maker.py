import pandas as pd
from core.extent_table import ExtentTable
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class TableMaker:
    ROOT_TABLE = "root"

    def __init__(self, extent_table: ExtentTable):
        self.__extent_table = extent_table

    def convert_json_objects_to_tables(self, json_objects: list, name: str) -> None:
        for json_object in json_objects:
            self.convert_json_object_to_table(json_object, name)

    def convert_json_object_to_table(self, json_object: dict, name: str) -> int:
        successfully_populated = self.__populate_table(json_object, name)

        if not successfully_populated:
            return -1

        current_id = self.__extent_table.get_current_id(name)

        self.__extent_table.increment_current_id(name)

        return current_id

    def __populate_table(self, json_object: dict, name: str) -> bool:
        successfully_populated = False
        for key, value in json_object.items():
            self.__add_values_to_table(name, key, value)
            successfully_populated = True
        return successfully_populated

    def __add_values_to_table(self, table_name: str, attribute: str, value) -> None:
        if self.__is_value_complex(value):
            self.__add_complex_value_to_table(table_name, attribute, value)
        elif self.__is_multivalued(value):
            self.__add_iterable_to_table(table_name, attribute, value)
        else:
            self.__add_scalar_value_to_table(table_name, attribute, value)

    def __add_complex_value_to_table(self, table_name: str, attribute: str, value: dict) -> None:
        reference_table_name = attribute
        reference_table_id = self.convert_json_object_to_table(value, reference_table_name)
        if reference_table_id >= 0:
            self.__extent_table.add_value(table_name, reference_table_name, reference_table_id)

    def __add_scalar_value_to_table(self, table_name: str, attribute: str, value) -> None:
        self.__extent_table.add_value(table_name, attribute, value)

    def __add_iterable_to_table(self, table_name: str, attribute: str, values: list) -> None:

        if len(values) == 0:
            return

        multivalued_table_name = table_name + "_?_" + attribute
        self.__extent_table.create_table(table_name)  # creates table if none existent
        columns = [ExtentTable.ID_COLUMN, ExtentTable.PARENT_COLUMN, ExtentTable.IS_SCALAR, ExtentTable.SCALAR_VALUE]
        self.__extent_table.create_table_from_columns(multivalued_table_name, columns)
        parent_table_current_id = self.__extent_table.get_current_id(table_name)
        rows = list()
        for value in values:
            row = dict.fromkeys(columns)
            if self.__is_value_complex(value):
                row[ExtentTable.ID_COLUMN] = self.__extent_table.get_current_id(multivalued_table_name)
                row[ExtentTable.PARENT_COLUMN] = str(parent_table_current_id)
                row[ExtentTable.IS_SCALAR] = False
                row[ExtentTable.SCALAR_VALUE] = None
                reference_table_name = self.__generate_table_name_from_complex_attribute(multivalued_table_name, value)
                value[ExtentTable.PARENT_COLUMN] = row[ExtentTable.ID_COLUMN]
                self.convert_json_object_to_table(value, reference_table_name)
            else:
                row[ExtentTable.ID_COLUMN] = self.__extent_table.get_current_id(multivalued_table_name)
                row[ExtentTable.PARENT_COLUMN] = str(parent_table_current_id)
                row[ExtentTable.IS_SCALAR] = True
                row[ExtentTable.SCALAR_VALUE] = str(value)
            rows.append(row)
            self.__extent_table.increment_current_id_pointer(multivalued_table_name)
        new_table = pd.DataFrame(rows)
        self.__extent_table.concat_tables(multivalued_table_name, new_table)

    def __is_multivalued(self, value) -> bool:
        return isinstance(value, list)

    def __is_value_complex(self, value) -> bool:
        return isinstance(value, dict)

    def show_tables(self, num_elements: int = 5) -> None:
        tables = self.__extent_table.get_all_tables()

        logging.info("\n")

        logging.info("SHOWING TABLES :D\n")

        for table_name, table in tables:
            logging.info("\nTable: " + table_name + "\n" + str(table.head(num_elements)) + "\n___________________\n\n")

    def save_tables(self, directory: str, export_as="csv", sql_connection=None) -> None:
        """
        :param sql_connection: the sql connection if you export as sql. Otherwise just ignore the parameter
        :param directory: the directory path for csv and html. For sql, pass in the root name share by all tables
        :param export_as: allowed values are: "csv", "sql", "html"
        :return: nothing
        """
        tables = self.__extent_table.get_all_tables()
        for table_name, table in tables:
            if export_as == "csv":
                table.to_csv(directory + table_name + "." + export_as, index=False)
            elif export_as == "sql":
                table.to_sql(directory + table_name, con=sql_connection)
            else:
                table.to_html(directory + table_name + "." + export_as, index=False)

    def __generate_table_name_from_complex_attribute(self, base_name: str, value: dict) -> str:
        keys = sorted(value.keys())
        return base_name + "_$_" + str(keys[0])
