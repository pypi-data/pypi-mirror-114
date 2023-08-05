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
import sqlite3
from typing import Sequence, Tuple, List


def run_sql(connection: sqlite3.Connection, sql: str, sql_values: Sequence = ()) -> Tuple[int, List]:
    """
    :param connection:  a SQLite3.Connection object
    :param sql:         the SQL to run with '?' for each input data location
    :param sql_values:  a Sequence of values to place in the '?' place holders.
    :return:            returns a 2 tuple containing lastrowid and results returned from the running of the SQL statement
    """
    cursor = connection.execute(sql, sql_values)
    result = cursor.fetchall()
    new_id = cursor.lastrowid
    return new_id, result
