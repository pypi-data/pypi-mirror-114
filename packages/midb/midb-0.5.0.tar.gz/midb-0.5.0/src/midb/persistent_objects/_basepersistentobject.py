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
midb.persistent_objects._basepersistentobject contains BasePersistentObject, a class that forms the base
for all persistent objects in midb. Most of the work of saving data to disk is done here.
"""

from typing import List, Any, Optional, Iterator, Sequence, cast, Type, ClassVar
from abc import ABC, abstractmethod
from midb.backend import SQLiteBackend
from midb.backend._serialization import get_class_id, SerializationPair, register_new_serialization_pair, _SERIALIZATION_FUNCTIONS

# the attributes that BasePersistentObject uses to store all others in the database.
# (note: mutmut changes strings and so that we do not have to create some convoluted test I'm just
# telling mutmut to skip mutating these strings.)
BACKEND_ATTR = '_backend'  # pragma: no mutate
ID_ATTR = '_id'  # pragma: no mutate
TEMP_ATTR = '_temp'  # pragma: no mutate
IN_MEMORY_CLASS_ATTR = '_in_memory_class'  # pragma: no mutate
RESERVED_ATTRIBUTES_ATTR = '_reserved_attributes' # pragma: no mutate


def register_persistent_object_class_with_serializer(cls: Type) -> Type:
    """
        A class decorator that will simply register the _string_serializer() and _string_deserializer()
        functions of the class as a SerializationPair simplifying the creation of Custom Persistent
        Object types.
    """
    register_new_serialization_pair(SerializationPair(cls, cls._string_serializer, cls._string_deserializer))
    return cls


def convert_if_necessary(value):
    """
        This function will convert an object to passed to it to it's matching persistent object type if one exists. If
        there is none it will return the value itself.
    """
    value_type = type(value)
    for cls_serialization_pair in _SERIALIZATION_FUNCTIONS.values():
        if (cls_serialization_pair.cls is not None
                and issubclass(cls_serialization_pair.cls, BasePersistentObject)
                and cls_serialization_pair.cls._in_memory_class == value_type):
            return cls_serialization_pair.cls(_init_temp=value)
    return value


class BasePersistentObject(ABC):
    """
        A BasePersistentObject emulates the type that is held in the _in_memory_class class attribute.

        When a new instance of a BasePersistentObject is created it may not be fully saved in the backend
        database so the data is held in the _temp attribute which is of the _in_memory_class type and all
        attribute access and method calls are proxied through that _temp object.

        If the _backend and _id the on disk database will be used for access and storage of data. In most cases
        a method call will pull the data for the object into memory using the in_memory() method (which returns
        a object of type _in_memory_class) and use the matching method of _in_memory_class to perform the function.

        If _backend is set but _id is not yet set then a new _id is created for the object and the data held in _temp
        is saved to the database and then set to None.
    """
    _backend: Optional[SQLiteBackend]
    _id: Optional[int]
    _temp: Any
    _in_memory_class: Type
    _reserved_attributes = [RESERVED_ATTRIBUTES_ATTR, ID_ATTR, BACKEND_ATTR, TEMP_ATTR, IN_MEMORY_CLASS_ATTR]

    def __init__(self, *, _init_temp: Any = None,
                 _backend:Optional[SQLiteBackend] = None, _id: Optional[int] = None) -> None:
        """
            Should be called from each subclass '__init__' method as:
            BasePersistentObject.__init__(self, _backend=_backend, _id=_id, _init_temp=_init_temp)
            each subclass should be able to take a '_backend' and '_id' argument and pass those along.
            '_init_temp' will be a temporary object that is created by the Subclass based on it's
            implementation.
        """
        # Warning:  Magic! It's important to set these in the proper order.
        #           Specifically that _backend is set last.
        #           * If _id is not set __setattr__ will create a new id and set
        #             _id to that value and then move the data in _temp to the
        #             backend db.
        #           * If _id is already set to some Non-None value before _backend
        #             is set then any value set in _temp will be ignored and set to
        #             None.
        self._id = _id
        self._init_temp(_init_temp)
        self._backend = _backend

    @abstractmethod
    def in_memory(self) -> Any:
        """
            Returns an object that contains all the attributes of the persistent object but in memory
            instead of on disk. This should be a shallow copy. (This must be implemented by each subclass.)
        """

    def __getattribute__(self, item: str) -> Any:
        """ implement self.item (the '.' operator). """
        try:
            # here we are using the super version of __getattribute__ to get any attributes
            # that are actually defined in the class or subclass.
            return super(BasePersistentObject, self).__getattribute__(item)
        except AttributeError as e:
            if item in self._reserved_attributes:
                # don't pass on reserved attributes to be handled by the in_memory object
                raise e
            # if the attribute is not defined then get it from the in-memory version that may have others
            # that are also defined. (Example 'PDict' uses the 'dict' types implementation of 'keys')
            in_memory = self.in_memory()
            if hasattr(in_memory, item):
                return getattr(in_memory, item)
            else:
                raise e

    @classmethod
    def _string_serializer(cls, obj: "BasePersistentObject") -> str:
        """ a simple string serializer for a persistent object used by the '_backend' object """
        if isinstance(obj, cls):
            return str(obj._id)
        else:
            raise ValueError(f"'{obj.__class__.__name__}' wrong class  for this serializer.('{cls.__class__.__name__}' expected)")

    @staticmethod
    def _string_deserializer(cls, string: str) -> "BasePersistentObject":
        """ a simple string deserializer for a persistent object used by the '_backend' object """
        return cls(_id=int(string))

    @abstractmethod
    def _init_temp(self, initial: Any) -> None:
        """
            This is called by '__init__' to initialize a temporary object.
            (This must be implemented by each subclass.)
        """

    def still_temp(self) -> bool:
        """
            Returns True if an object is not fully initialized (and data is still being
            held in the '_temp' object) and False if it has been.
        """
        return (not hasattr(self, BACKEND_ATTR) or
                self._backend is None or
                not hasattr(self, ID_ATTR) or
                self._id is None)

    @abstractmethod
    def _get_temp(self, key: Any) -> Any:
        """
            Used by '_get' when an object is not fully initialized
            and data is still being held in the '_temp' object.
            (This must be implemented by each subclass.)
        """

    @abstractmethod
    def _move_temp_to_backend(self) -> None:
        """
            When an object has been fully initialized this is called to move what is being held in '_temp'
            into the database. (This must be implemented by each subclass.)
        """

    def _get(self, key: Any) -> Any:
        """ Does the heavy lifting of retrieving a value from the database using the key and the '_id' of the object """
        key = convert_if_necessary(key)
        if self.still_temp():
            return self._get_temp(key)
        else:
            _backend = cast(SQLiteBackend, self._backend)
            _id = cast(int, self._id)
            value = _backend.get(_id, key)
            return value

    def __setattr__(self, key: Any, value: Any) -> None:
        """
            Called when setting an attribute (self.key = value)
        """
        is_property_descriptor = False # pragma: no mutate
        try:
            if type(self.__class__.__dict__[key]) is property:
                is_property_descriptor = True
        except:
            pass
        if key in self._reserved_attributes or is_property_descriptor:
            if (key == TEMP_ATTR and value is not None) and not self.still_temp():
                # do not set _temp if object is fully initialized
                return
            elif key == BACKEND_ATTR and not ((type(value) is SQLiteBackend) or (value is None)):
                # do not set _backend if the value is not a SQLiteBackend
                return
            super(BasePersistentObject, self).__setattr__(key, value)
            if key == BACKEND_ATTR and value is not None:
                backend = cast(SQLiteBackend, self._backend)
                if self._id is None:
                    # if the '_backend' attribute is being set but the _id has not been set then we need to create a
                    # new persistent object id, set that to the '_id' attribute, and move the contents of _temp into
                    # the database.
                    self._id = backend.add_new_persistent_object(self)
                    self._move_temp_to_backend()
                else:
                    # if _id is set and the _backend attribute is being set then we need to ignore any data
                    # that is in _temp by setting it to None
                    self._temp = None
        else:
            self._not_reserved_setattr(key, value)

    def _not_reserved_setattr(self, key: Any, value: Any) -> None:
        """
            This must be implemented by each subclass and is called by "__setattr__" to give the Subclass a chance to
            do something that it sees as appropriate but by default we will raise an AttributeError
        """
        raise AttributeError(f'{self.__class__.__name__} object has no attribute {key}')

    @abstractmethod
    def _set_temp(self, key: Any, value: Any) -> None:
        """
            Used by '_set' when the object is not fully initialized
            and data is still being held in the '_temp' object.
            (This must be implemented by each subclass.)
        """

    def _set(self, key: Any, value: Any, commit: bool = True) -> None:
        """ Does the heavy lifting of setting a value in the database using the key and the '_id' of the object """
        key = convert_if_necessary(key)
        value = convert_if_necessary(value)
        if self.still_temp():
            self._set_temp(key, value)
        else:
            _backend = cast(SQLiteBackend, self._backend)
            _id = cast(int, self._id)
            if isinstance(value, BasePersistentObject) and not value.still_temp() and value._backend != self._backend:
                # this is the case where a value that is a persistent object lives in a different backend.
                # in this case copy the contents from the values original database in to the current objects database.
                value2 = value.__class__(_init_temp=value.in_memory())
                value = value2
            _backend.set(_id, key, value, commit)

    @abstractmethod
    def _del_temp(self, key: Any) -> None:
        """
            Used by '_del' when the object is not fully initialized
            and data is still being held in the '_temp' object.
            (This must be implemented by each subclass.)
        """

    def _del(self, key: Any, commit: bool = True) -> None:
        """
            deletes key from database. 'commit' can be set to False when this is being called as part of a more involved
            process to speed up the database and make that process atomic.
        """
        key = convert_if_necessary(key)
        if self.still_temp():
            self._del_temp(key)
        else:
            _backend = cast(SQLiteBackend, self._backend)
            _id = cast(int, self._id)
            _backend.delete(_id, key, commit)

    # using in_memory types implementation of the following functions, will reimplement any when necessary
    def __contains__(self, item: Any, /) -> bool:
        """ implement: key in self """
        for item_in in self:
            if item == item_in:
                return True
        return False

    def __eq__(self, value: Any, /) -> bool:
        """ implement: self == value """
        if isinstance(value, BasePersistentObject):
            value = value.in_memory()
        return self.in_memory() == value

    def __ge__(self, value: Any, /) -> bool:
        """ implement: self >= value """
        comp_value = value
        if isinstance(value, BasePersistentObject):
            comp_value = value.in_memory()

        try:
            return self.in_memory() >= comp_value
        except TypeError:
            raise TypeError(
                f"'>=' not supported between instances of '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __gt__(self, value: Any, /) -> bool:
        """ implement: self > value """
        comp_value = value
        if isinstance(value, BasePersistentObject):
            comp_value = value.in_memory()

        try:
            return self.in_memory() > comp_value
        except TypeError:
            raise TypeError(
                f"'>' not supported between instances of '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __iter__(self, /) -> Iterator:
        """ implement: iter(self) """
        return iter(self.in_memory())

    def __le__(self, value: Any, /) -> bool:
        """ implement: self <= value """
        comp_value = value
        if isinstance(value, BasePersistentObject):
            comp_value = value.in_memory()

        try:
            return self.in_memory() <= comp_value
        except TypeError:
            raise TypeError(
                f"'<=' not supported between instances of '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __len__(self, /) -> int:
        """ implement: len(self) """
        return len(self.in_memory())

    def __lt__(self, value: Any, /) -> bool:
        """ implement: self < value """
        comp_value = value
        if isinstance(value, BasePersistentObject):
            comp_value = value.in_memory()

        try:
            return self.in_memory() < comp_value
        except TypeError:
            raise TypeError(
                f"'<' not supported between instances of '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __ne__(self, value: Any, /) -> bool:
        """ implement: self != value """
        if isinstance(value, BasePersistentObject):
            value = value.in_memory()
        return self.in_memory() != value

    def __repr__(self, /) -> str:
        """ implement: repr(self) """
        if hasattr(self, BACKEND_ATTR):
            backend = f"_backend={self._backend}"
        else:
            backend = f"(_backend not set)"
        if hasattr(self, ID_ATTR):
            id_ = f"_id={self._id}"
        else:
            id_ = f"(_id not set)"
        if hasattr(self, TEMP_ATTR):
            temp = f"_temp={self._temp}"
        else:
            temp = f"(_temp not set)"
        try:
            contents = self.in_memory()
        except ValueError:
            contents = "(no contents)"

        return f'{self.__class__.__name__}({contents}, {backend}, {id_}, {temp})'

    def __reversed__(self, /) -> Iterator:
        """ implement: reversed(self) """
        return reversed(self.in_memory())