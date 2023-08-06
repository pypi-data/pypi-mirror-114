"""
Tests database tools
"""
import pathlib
import unittest
from pathlib import Path
import threading
from typing import List, Tuple

from hein_control.db_tools import DatabaseTable

lock = threading.Lock()


def run_locked(func):
    """decorator to run a function using a lock"""
    def wrapper(*args, **kwargs):
        with lock:
            func(*args, **kwargs)
    return wrapper


class TestDatabaseTable(DatabaseTable):
    @property
    def table_name(self) -> str:
        return 'TEST_DB_TABLE'

    @property
    def column_name_types(self) -> List[Tuple[str, str]]:
        return [
            ('col_1', 'TEXT'),
            ('col_2', 'REAL'),
            ('col_3', 'BOOL'),
        ]


class AnotherTestDatabaseTable(DatabaseTable):
    @property
    def column_name_types(self) -> List[Tuple[str, str]]:
        return [
            ('col_1', 'TEXT'),
            ('col_2', 'REAL'),
            ('col_3', 'BOOL'),
        ]

    @property
    def table_name(self) -> str:
        return 'ANOTHER_TEST_DB_TABLE'


class TestDBTools(unittest.TestCase):

    db_path = 'test_db.db'
    db_table = None

    def setUp(self) -> None:
        if Path(self.db_path).exists():
            # delete any existing db files
            Path(self.db_path).unlink()
        self.db_table = TestDatabaseTable(file_path=self.db_path)

    def test_db_extension(self):
        """tests db basic setting"""
        self.assertIsInstance(self.db_table.file_path, pathlib.Path, 'ensure table path is pathlib.Path')
        self.assertEqual(self.db_table.file_path.suffix, '.db', 'ensure extension exists')

    @run_locked
    def test_db_basic_properties(self):
        table_names = self.db_table.db_table_names
        self.assertEqual(1, len(table_names), 'there should only be 1 table in the database')
        self.assertEqual('TEST_DB_TABLE', table_names[0], 'the database table name should match')

        column_names = self.db_table.column_names
        self.assertEqual(3, len(column_names), 'there should only be 3 columns in the database')
        for index in range(3):
            col_number = index + 1
            self.assertEqual(f'col_{col_number}', column_names[index])

    def test_adding_second_table(self):
        # test adding a second table to the database
        another_db_table = AnotherTestDatabaseTable(file_path=self.db_path)

        table_names = another_db_table.db_table_names
        self.assertEqual(2, len(table_names), 'there should only be 2 tables in the database')
        self.assertEqual(['TEST_DB_TABLE', 'ANOTHER_TEST_DB_TABLE'], table_names,
                         'the database table names should match')

    def test_basic_protection(self):
        """tests the basic sqlite injection prevention"""
        for attr in ['_base_query', 'table_name']:
            self.assertRaises(
                AttributeError,
                setattr,
                self.db_table,
                attr,
                'malicious value'
            )


