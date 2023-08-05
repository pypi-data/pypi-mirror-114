# MIT License
#
# Copyright (c) 2021 Peter Goss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
    midb.backend._db_creation_and_validation handles the creation ond validation of midb SQLite databases.
"""
import sqlite3
from midb.constants import MEMORY_DB, DEFAULT_ROOT_CLASS_ID
from midb.backend._serialization import ClassID
from midb.backend._run_sql import run_sql


def create_db(filename: str = MEMORY_DB, root_obj_class_id: ClassID = DEFAULT_ROOT_CLASS_ID) -> sqlite3.Connection:
    """
    :param filename:            the filename of where the SQLite database will be stored
    :param root_obj_class_id:   the class object id (as returned by midb.backend._serialization.get_class_id())
                                    of the object to be used as the root object (id=0).
    :return:                    returns a connection to the database
    """
    con = sqlite3.connect(filename)
    run_sql(con, "PRAGMA journal_mode=WAL")
    # self.run_sql('PRAGMA foreign_keys = ON')
    run_sql(con, "CREATE TABLE IF NOT EXISTS persistent_objects (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT)")
    run_sql(con, "CREATE TABLE IF NOT EXISTS  key_value ("
                      "parent_id INTEGER, "
                      "key_hash INTEGER, "
                      "key_type TEXT, "
                      "key TEXT, "
                      "value_type TEXT, "
                      "value TEXT)")
    values = [root_obj_class_id]
    run_sql(con, "INSERT OR REPLACE INTO persistent_objects VALUES (0, ?)", sql_values=values)
    con.commit()
    return con


def valid_db(connection: sqlite3.Connection) -> bool:
    """
    returns True if a properly constructed database is found.
    return False if necessary tables are missing (correctable).
    raises ValueError in necessary tables exist but are structured incorrectly (not correctable)
    """
    persistent_objects_table_exists = _persistent_objects_table_exists(connection)
    persistent_objects_table_valid = _persistent_objects_table_valid(connection)
    persistent_objects_table_has_root_record = _persistent_objects_table_has_root_record(connection)
    key_value_table_exists = _key_value_table_exists(connection)
    key_value_table_valid = _key_value_table_valid(connection)

    if (
            persistent_objects_table_exists
            and persistent_objects_table_valid
            and persistent_objects_table_has_root_record
            and key_value_table_exists
            and key_value_table_valid
    ):
        return True
    elif ((persistent_objects_table_exists and not persistent_objects_table_valid)
            or
            (key_value_table_exists and not key_value_table_valid)):
        raise ValueError("incompatible database.")
    else:
        return False


# Persistent Object Table validation
def _persistent_objects_table_exists(connection: sqlite3.Connection) -> bool:
    _, result = run_sql(connection, "SELECT tbl_name FROM sqlite_master WHERE tbl_name IS 'persistent_objects'")
    if len(result) > 0:
        return True
    else:
        return False


def _persistent_objects_table_valid(connection: sqlite3.Connection) -> bool:
    _, result = run_sql(connection, "SELECT sql FROM sqlite_master WHERE tbl_name IS 'persistent_objects'")
    try:
        if result[0][0] == "CREATE TABLE persistent_objects (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT)":
            return True
    except IndexError:
        pass
    return False


def _persistent_objects_table_has_root_record(connection: sqlite3.Connection) -> bool:
    try:
        _, result = run_sql(connection, "SELECT * FROM persistent_objects WHERE id = 0")
        if len(result) == 1:
            return True
    except sqlite3.OperationalError:
        pass
    return False


# Key_Value Table validation
def _key_value_table_exists(connection: sqlite3.Connection) -> bool:
    _, result = run_sql(connection, "SELECT tbl_name FROM sqlite_master WHERE tbl_name IS 'key_value'")
    if len(result) > 0:
        return True
    else:
        return False


def _key_value_table_valid(connection: sqlite3.Connection) -> bool:
    _, result = run_sql(connection, "SELECT sql FROM sqlite_master WHERE tbl_name IS 'key_value'")
    try:
        if result[0][0] == ("CREATE TABLE key_value ("
                                "parent_id INTEGER, "
                                "key_hash INTEGER, "
                                "key_type TEXT, "
                                "key TEXT, "
                                "value_type TEXT, "
                                "value TEXT)"):
            return True
    except IndexError:
        pass
    return False

