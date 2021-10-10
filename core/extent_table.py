import pandas as pd
from typing import Tuple
from typing import List
import logging
import pickle
from pathlib import Path
import os


class ExtentTable:
    ID_COLUMN = "ID"

    IS_SCALAR = "is_scalar"

    IS_COMPLEX = "is_complex"

    SCALAR_VALUE = "scalar"

    COMPLEX_VALUE = "complex"

    PARENT_COLUMN = "PARENT_ID"

    def __init__(self):
        self.__tables = dict()

        self.__current_ids = dict()

    def save_extent_table_state(self, directory_path: str = "extent_table_state") -> None:
        Path(directory_path).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(directory_path, "tables.pkl"), "wb") as fp:
            pickle.dump(self.__tables, fp, pickle.HIGHEST_PROTOCOL)

        with open(os.path.join(directory_path, "current_ids.pkl"), "wb") as fp:
            pickle.dump(self.__current_ids, fp, pickle.HIGHEST_PROTOCOL)

    def load_extent_table_state(self, directory_path: str = "extent_table_state") -> None:
        with open(os.path.join(directory_path, "tables.pkl"), "rb") as fp:
            self.__tables = pickle.load(fp)

        with open(os.path.join(directory_path, "current_ids.pkl"), "rb") as fp:
            self.__current_ids = pickle.load(fp)

    def get_extent(self) -> dict:
        return self.__tables

    def add_column(self, name: str, attribute: str) -> None:
        if name not in self.__tables:
            self.create_table(name)

        if attribute not in self.__tables[name].columns:
            self.__tables[name][attribute] = [None] * self.__tables[name].shape[0]

    def add_value(self, name: str, attribute: str, value) -> None:
        self.add_column(name, attribute)

        self.__tables[name].loc[self.get_current_id(name), attribute] = str(value)

    def get_next_id(self, name: str) -> int:
        return self.__current_ids[name] + 1

    def get_current_id(self, name: str) -> int:
        return self.__current_ids[name]

    def increment_current_id(self, name) -> None:
        self.__current_ids[name] += 1

        columns = self.__tables[name].columns

        empty_row = dict()

        for key in columns:
            empty_row[key] = None

        empty_row[ExtentTable.ID_COLUMN] = self.__current_ids[name]

        table = pd.DataFrame([empty_row])

        self.concat_tables(name, table)

    def increment_current_id_pointer(self, name) -> None:
        self.__current_ids[name] += 1

    def add_table(self, name: str, table: pd.DataFrame) -> None:
        self.__tables[name] = table

    def create_table(self, name: str) -> None:
        if name in self.__tables:
            logging.warning("Table already exists")

            return

        table = pd.DataFrame()

        table[ExtentTable.ID_COLUMN] = [0]

        self.add_table(name, table)

        self.__current_ids[name] = 0

    def create_table_from_columns(self, name: str, columns: list) -> None:
        if name in self.__tables:
            return
        table = pd.DataFrame(columns=columns)

        self.add_table(name, table)

        self.__current_ids[name] = 0

    def concat_tables(self, name: str, table: pd.DataFrame) -> None:
        new_table = pd.concat([self.__tables[name], table]).reset_index(drop=True)

        self.__tables[name] = new_table

    def get_table(self, name) -> pd.DataFrame:
        return self.__tables[name]

    def get_all_tables(self) -> List[Tuple[str, pd.DataFrame]]:
        tables = list()
        for table_name, table in self.__tables.items():
            tables.append((table_name, table))

        return tables

    def trim_last_rows(self) -> None:
        table_names = self.__tables.keys()

        for table_name in table_names:
            self.trim_last_row_from_table(table_name)

    def trim_last_row_from_table(self, name) -> None:
        self.__tables[name].drop(self.__tables[name].tail(1).index, inplace=True)

        self.__current_ids[name] -= 1
