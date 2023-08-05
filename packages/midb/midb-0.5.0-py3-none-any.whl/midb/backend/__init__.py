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
midb.backend is where all the interaction with the SQLite database takes place.
"""
from typing import Sequence, List, Tuple, Any, Union, cast
from abc import ABCMeta
import sqlite3

import midb
from midb.constants import MEMORY_DB, DEFAULT_ROOT_CLASS_ID
from midb.backend._serialization import ClassID, get_class_id
from midb.backend._serialization import serialize, deserialize
from midb.backend._db_creation_and_validation import valid_db, create_db
from midb.backend._run_sql import run_sql


class SQLiteBackend:
    """
    An SQLiteBackend object maintains a connection to the database in use together with other information
    related to the state. It is used as the way to interact with the database.
    """
    def __init__(self,
                 filename: str = MEMORY_DB,
                 root_class: Union[ClassID, type] = DEFAULT_ROOT_CLASS_ID,
                 auto_commit: bool = True):

        self.filename = filename
        self.auto_commit = auto_commit
        self.connection = sqlite3.connect(self.filename)

        if not valid_db(connection=self.connection):
            root_class_id: ClassID
            if type(root_class) is ClassID:
                root_class = cast(ClassID, root_class)
                root_class_id = root_class
            else:
                root_class_id = get_class_id(root_class)
            self.connection = create_db(filename, root_class_id)

    def __repr__(self):
        """
        Return repr(self).
        """
        return f'{self.__class__.__name__}(filename="{self.filename}")'

    def __str__(self):
        """
        Return str(self).
        """
        return self.__repr__()

    def commit(self) -> None:
        """ performs a commit on the SQL connection. """
        self.connection.commit()

    def commit_if_auto(self) -> None:
        """ Performs a commit if the database is setup to perform auto-commits (default) """
        if self.auto_commit:
            self.commit()

    # PERSISTENT OBJECT METHODS #
    def add_new_persistent_object(self, persistent_object: "midb.BasePersistentObject", commit=True) -> int:
        """ creates a new record for a new Persistent Object and returns it's id. """
        class_id = get_class_id(persistent_object)
        new_id, _ = run_sql(self.connection, "INSERT INTO persistent_objects (type) VALUES (?)", [class_id])
        if commit:
            self.commit_if_auto()
        return new_id

    @property
    def root(self) -> "midb.persistent_objects.BasePersistentObject":
        """ returns the root object for the database. """
        sql = "SELECT id, type from persistent_objects WHERE id = 0"
        _, result = run_sql(self.connection, sql)
        root_serialization_string = result[0][0]
        root_class_id = result[0][1]
        return_root = self._deserialize_and_set_backend_if_necessary(root_class_id, root_serialization_string)
        return return_root

    def _deserialize_and_set_backend_if_necessary(self, class_id_str, serialization_str):
        """
            A common need is to set the _backend attribute if the object that is deserialized is of a type that is a
            subclass of BasePersistentObject. This function takes care of that.
        """
        result = deserialize(class_id_str, serialization_str)
        if isinstance(result, midb.BasePersistentObject):
            result._backend = self
        return result

    def _get_equivalent_key_or_same(self, parent_id: int, key: Any) -> Any:
        """
            A key is considered equivalent if it both has the same hash and tests as equal.
            This function will do a look up in the database to see if there is already a key
            in the parent that is equivalent and returns that key, otherwise it will return
            the value given to it. This will raise a TypeError if the key argument is not
            hashable.
        """
        sql = "SELECT key_type, key FROM key_value WHERE parent_id IS ? and key_hash IS ?"
        sql_values = [parent_id, hash(key)]
        _, results = run_sql(self.connection, sql, sql_values)
        for row in results:
            same_hash_key = self._deserialize_and_set_backend_if_necessary(*row)
            if same_hash_key == key:
                if isinstance(key, midb.BasePersistentObject) and key._id == same_hash_key._id:
                    return key
                else:
                    return same_hash_key
        return key

    # KEY_VALUE METHODS #
    def get(self, parent_id: int, key: Any) -> Any:
        """ from the parent object id and the key object return the value held there. """
        key = self._get_equivalent_key_or_same(parent_id, key)
        sql = "SELECT value_type, value FROM key_value where parent_id IS ? AND key_type IS ? AND key IS ?"
        sql_values = [parent_id, *serialize(key)]
        _, result = run_sql(self.connection, sql, sql_values)
        if len(result) > 0:
            return_value = self._deserialize_and_set_backend_if_necessary(*result[0])
            return return_value

        else:
            raise KeyError(str(key))

    def key_exists(self, parent_id: int, key: Any) -> bool:
        """ returns True if a key (or equivalent) exists in the parent object and False otherwise. """
        try:
            self.get(parent_id, key)
        except KeyError:
            return False
        return True

    def _number_of_records_that_a_persistent_object_is_in(self, persistent_object: "midb.BasePersistentObject"):
        """
            Returns the number of key/value records that a persistent object is in. If a persistent object is in
            both the key and value position in a key/value record this only counts as one.
        """
        sql = "SELECT * from key_value WHERE (key_type=? AND key=?) OR (value_type=? AND value=?)"
        sql_values = [*serialize(persistent_object), *serialize(persistent_object)]
        _, results = run_sql(self.connection, sql, sql_values)
        return len(results)

    def _delete_persistent_object(self, persistent_object: "midb.BasePersistentObject"):
        """
            Deletes the data for the given persistent object from the database and returns the persistent object to
            a temp state. It is the responsibility of the caller to make sure there are no references to this object
            in the key_value table.
        """
        contents = persistent_object.in_memory()
        obj_id = persistent_object._id
        sql = "DELETE FROM key_value WHERE parent_id IS ?"
        sql_values = [obj_id]
        run_sql(self.connection, sql, sql_values)
        sql = "DELETE FROM persistent_objects WHERE id IS ?"
        run_sql(self.connection, sql, sql_values)
        persistent_object._id = None
        persistent_object._backend = None
        persistent_object._temp = contents

    def set(self, parent_id: int, key: Any, value: Any, commit: bool = True) -> None:
        """ sets a parent objects key to the value provided. """
        key = self._get_equivalent_key_or_same(parent_id, key)
        if isinstance(key, midb.BasePersistentObject) and key.still_temp():
            key._backend = self  # this saves the key to the db if it has not been created yet.
        if isinstance(value, midb.BasePersistentObject) and value.still_temp():
            value._backend = self # this saves the key to the db if it has not been created yet.
        if self.key_exists(parent_id, key):
            # update value in key/value pair
            current_value = self.get(parent_id, key)
            if (isinstance(current_value, midb.BasePersistentObject)  # if the value is a persistent object
                    and self._number_of_records_that_a_persistent_object_is_in(current_value) == 1  # and it is only involved in one record
                    and current_value != key):  # but the value does not also equal the key
                self._delete_persistent_object(current_value)  # then delete it from the database before replacing it.

            sql = ("UPDATE key_value SET value_type = ? , value = ? "
                   "WHERE parent_id = ? AND key_hash = ? AND key_type = ? AND  key = ?")
            sql_values = [*serialize(value), parent_id, hash(key), *serialize(key)]
            run_sql(self.connection, sql, sql_values)
        else:
            # insert new key/value pair
            sql = "INSERT INTO key_value VALUES (?, ?, ?, ?, ?, ?)"
            sql_values = [parent_id, hash(key), *serialize(key), *serialize(value)]
            run_sql(self.connection, sql, sql_values)
        if commit:
            self.commit_if_auto()

    def delete(self, parent_id: int, key: Any, commit: bool = True) -> None:
        """ deletes the provided key from the parent """
        key = self._get_equivalent_key_or_same(parent_id, key)
        current_value = self.get(parent_id, key)
        if (isinstance(key, midb.BasePersistentObject)
                and self._number_of_records_that_a_persistent_object_is_in(key) == 1):
            self._delete_persistent_object(key)
        if (isinstance(current_value, midb.BasePersistentObject)
                and self._number_of_records_that_a_persistent_object_is_in(current_value) == 1):
            self._delete_persistent_object(current_value)

        sql = "DELETE FROM key_value WHERE parent_id IS ? AND key_type IS ? AND key IS ?"
        sql_values = [parent_id, *serialize(key)]
        run_sql(self.connection, sql, sql_values)
        if commit:
            self.commit_if_auto()

    def delete_all_children(self, parent_id: int, commit: bool = True):
        """ deletes all keys from a parent. """
        keys = self.get_keys(parent_id)
        for key in keys:
            self.delete(parent_id, key, commit=False)
        if commit:
            self.commit_if_auto()

    def get_keys(self, parent_id: int) -> List:
        """ returns a list of all the keys contained in the parent """
        sql = "SELECT key_type, key FROM key_value WHERE parent_id IS ?"
        sql_values = [parent_id]
        _, results = run_sql(self.connection, sql, sql_values)
        return_keys = []
        for row in results:
            new_key = self._deserialize_and_set_backend_if_necessary(*row)
            return_keys.append(new_key)
        return return_keys

    def get_values(self, parent_id: int) -> List:
        """ returns all the values held in they keys of the parent """
        sql = "SELECT value_type, value FROM key_value WHERE parent_id IS ?"
        sql_values = [parent_id]
        _, results = run_sql(self.connection, sql, sql_values)
        return_values = []
        for row in results:
            new_value = self._deserialize_and_set_backend_if_necessary(*row)
            return_values.append(new_value)
        return return_values

    def get_items(self, parent_id: int) -> Any:
        """ returns a tuple of 2 tuples containing all the key-value pairs in the parent """
        sql = "SELECT key_type, key, value_type, value FROM key_value WHERE parent_id IS ?"
        sql_values = [parent_id]
        _, results = run_sql(self.connection, sql, sql_values)
        return_values = []
        for row in results:
            key_type_id = row[0]
            key_serialization_str = row[1]
            value_type_id = row[2]
            value_serialization_str = row[3]
            key = self._deserialize_and_set_backend_if_necessary(key_type_id, key_serialization_str)
            value = self._deserialize_and_set_backend_if_necessary(value_type_id, value_serialization_str)
            return_values.append((key, value))
        return return_values

    # methods for manipulating lists stored in dictionary style key/value store.
    def list_shift(self, list_id: int, shift_start: int, shift_by: int, commit: bool = True) -> None:
        """
            Shifts keys of the list like persistent object with id of 'list_id' starting from 'shift_start' and shifting
            by 'shift_by'. Useful for deleting items from or inserting items to list like persistent objects.
        """
        sql = ("UPDATE key_value "
               "SET key = cast((cast(key AS Integer) + ?) AS Text) "
               "WHERE parent_id = ? AND cast(key AS Integer) >= ?")
        sql_values = [shift_by, list_id, shift_start]
        run_sql(self.connection, sql, sql_values)
        if commit:
            self.commit_if_auto()

    def list_del_item(self, list_id: int, index: int, commit: bool = True) -> None:
        """
            For list like persistent objects. This will delete from object with id of 'list_id' the item with key
            'index' and then subtracts 1 from all keys larger than 'index'.
        """
        self.delete(list_id, index, commit=False)
        self.list_shift(list_id, index + 1, -1, commit=False)
        if commit:
            self.commit_if_auto()

    def list_insert(self, list_id: int, index: int, value: Any, commit: bool = True) -> None:
        """
            For list like persistent objects. In object with id of 'list_id' adds 1 to all keys greater than or equal to
            'index' and then inserts 'value' to key value 'index'.
        """
        if type(index) is not int:
            raise TypeError(f"integer argument expected, got '{type(index).__name__}'")
        self.list_shift(list_id, index, 1, commit=False)
        self.set(list_id, index, value, commit=False)
        if commit:
            self.commit_if_auto()

    def list_del_multiple(self, list_id: int, indices: List[int], commit: bool = True) -> None:
        """
             For list like persistent objects. This will delete from object with id of 'list_id' all items with keys
             in indices list using 'list_del_item'. This is used by PList when deleting a slice.
        """
        indices.sort(reverse=True)
        for i in indices:
            self.list_del_item(list_id, i, commit=False)
        if commit:
            self.commit_if_auto()