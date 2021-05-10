import sqlite3
import contextlib
import os
from typing import Any, Iterable
from dotenv import load_dotenv


load_dotenv()


class SQLite:
    SQLITE_FILE_NAME = os.getenv('SQLITE_FILE_NAME')
    SQLITE_TABLE_GROUP_NAME = os.getenv('SQLITE_TABLE_GROUP_NAME')

    def __init__(self):
        if not self.has_table_exists(self.SQLITE_TABLE_GROUP_NAME):
            self.__execute_select("CREATE TABLE {0} (gid text)".format(self.SQLITE_TABLE_GROUP_NAME))

    def __execute_select(self, statement: str, parameters: Iterable[Any] = ()):
        """https://stackoverflow.com/a/46519449"""
        with contextlib.closing(sqlite3.connect(self.SQLITE_FILE_NAME)) as connect, connect, \
                contextlib.closing(connect.cursor()) as cursor:
            cursor.execute(statement, parameters)

            return cursor.fetchall()

    def __execute_mutable(self, statement: str, parameters: Iterable[Any] = ()):
        with contextlib.closing(sqlite3.connect(self.SQLITE_FILE_NAME)) as connect, connect, \
                contextlib.closing(connect.cursor()) as cursor:
            cursor.execute(statement, parameters)
            connect.commit()

            return cursor.lastrowid

    def has_table_exists(self, table_name: str):
        result = self.__execute_select(
            "SELECT count(name) FROM sqlite_master WHERE type=? AND name=?",
            ('table', table_name,)
        )

        return result[0][0] != 0

    def has_row_exists(self, table_name: str, where: str, parameters: Iterable[Any]):
        result = self.__execute_select(
            "SELECT EXISTS(SELECT 1 FROM {0} WHERE {1})".format(table_name, where),
            parameters
        )

        return result[0][0] != 0

    def add_group(self, gid: str):
        if not self.has_row_exists('groups', 'gid=?', (gid,)):
            self.__execute_mutable(
                "INSERT INTO {0}(gid) VALUES(?)".format(self.SQLITE_TABLE_GROUP_NAME),
                (gid,)
            )

            return True

        return False

    def get_groups(self):
        result = self.__execute_select("SELECT gid FROM {0}".format(self.SQLITE_TABLE_GROUP_NAME))

        return result
