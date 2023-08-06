"""
Module for interacting with an SQLite3 database (.db files)
"""
import sqlite3
import pathlib

from abc import ABC, abstractmethod
from typing import List, Tuple, Union
from contextlib import closing


def get_db_table_names(file_path: str) -> List[str]:
    """Return a list of table names, given the database path"""
    with sqlite3.connect(file_path) as db:
        with closing(db.cursor()) as cur:
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [names[0] for names in cur.fetchall()]
    return table_names


def get_db_column_names(file_path, table_name: str) -> List[str]:
    """Return a list of the column names for a table in a database, given the database path"""
    raise NotImplementedError('access the get_table_column_names method of DatabaseTable')


class DatabaseTable(ABC):
    def __init__(self, file_path: Union[str, pathlib.Path]):
        """
        Create a SQLite3 table at the database at the path with the columns if it doesnt already exist

        This is a SQLite3 database table mixin. To use, subclass this class and define the table_name and
        column_name_types. Basic sql injection attack prevention is provided by disallowing the user to set the
        table name and column definitions (defined when the class is defined). There is no protection against imporper
        definition of the subclasses.

        :param file_path: path to the database (.db file)
        """
        self._file_path: pathlib.Path = None
        self.file_path = file_path

        # create table if it does not exist
        commands = []
        # build command and parameters so that they can be executed safely
        for name, value_type in self.column_name_types:
            commands.append(f'{name} {value_type}')
        table_structure = ', '.join(commands)
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                # create the table
                cur.execute(
                    f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_structure})',
                )
            db.commit()

        self.column_names: List[str] = self.get_table_column_names()

    @property
    def file_path(self) -> pathlib.Path:
        """Path to the database .db file"""
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if value is not None:
            if isinstance(value, pathlib.Path) is False:
                value = pathlib.Path(value)
            if value.suffix != '.db':
                value = value.parent / (value.name + '.db')
            self._file_path = value

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Name of the table in the database"""
        raise NotImplementedError

    @property
    @abstractmethod
    def column_name_types(self) -> List[Tuple[str, str]]:
        """defines the column names and types to be used if the table needs to be created"""
        raise NotImplementedError

    @property
    def _base_query(self) -> str:
        """the base query for the instance. This provides a basic security layer between the user and the query for
        avoiding sql injections"""
        return f'select * from {self.table_name}'

    @property
    def db_table_names(self) -> List[str]:
        """A list of the name of all tables in the database"""
        names = get_db_table_names(file_path=self.file_path)
        return names

    def get_table_column_names(self) -> List[str]:
        """Return a list of the column names for a table in a database, given the database path"""
        with sqlite3.connect(self.file_path) as db:
            with closing(db.cursor()) as cur:
                # todo scrub for sql injection
                cur.execute(self._base_query)
                column_names = [description[0] for description in cur.description]
        return column_names
