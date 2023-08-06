# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.MapSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Map schema implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, List

from pip_services3_commons.validate import IValidationRule
from .Schema import Schema
from .ValidationResult import ValidationResult
from .ValidationResultType import ValidationResultType
from ..reflect.ObjectReader import ObjectReader


class MapSchema(Schema):
    """
    Schema to validate maps.

    Example:

    .. code-block:: python

        schema = MapSchema(TypeCode.String, TypeCode.Integer)
        schema.validate({ "key1": "A", "key2": "B" })       # Result: no errors
        schema.validate({ "key1": 1, "key2": 2 })           # Result: element type mismatch
        schema.validate([ 1, 2, 3 ])                        # Result: type mismatch
    """
    __key_type: Any = None
    __value_type: Any = None

    def __init__(self, key_type: Any = None, value_type: Any = None, required: bool = None,
                 rules: List[IValidationRule] = None):
        """
        Creates a new instance of validation schema and sets its values.

        :param key_type: a type of map keys. Null means that keys may have any type.
        :param value_type: a type of map values. Null means that values may have any type.
        :param required: (optional) true to always require non-null values.
        :param rules: (optional) a list with validation __rules.
        """
        super(MapSchema, self).__init__(required, rules)
        self.__key_type = key_type
        self.__value_type = value_type

    def get_key_type(self) -> Any:
        """
        Gets the type of map keys.
        None means that keys may have any type.

        :returns: the type of map keys.
        """
        return self.__key_type

    def set_key_type(self, value: Any):
        """
        Sets the type of map keys.
        None means that keys may have any type.

        :param value: a type of map keys.
        """
        self.__key_type = value

    def get_value_type(self) -> Any:
        """
        Gets the type of map values.
        None means that values may have any type.

        :return: the type of map values.
        """
        return self.__value_type

    def set_value_type(self, value: Any):
        """
        Sets the type of map values.
        Null means that values may have any type.

        :return: a type of map values.
        """
        self.__value_type = value

    def _perform_validation(self, path: str, value: Any, results: List[ValidationResult]):
        """
        Validates a given args against the schema and configured validation __rules.

        :param path: a dot notation path to the args.

        :param value: a args to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if not (path is None) else "args"
        value = ObjectReader.get_value(value)

        super(MapSchema, self)._perform_validation(path, value, results)

        if value is None:
            return

        if isinstance(value, dict):
            for (key, value) in value.items():
                element_path = key if path is None or len(path) == 0 else path + "." + key

                self._perform_type_validation(element_path, self.__key_type, key, results)
                self._perform_type_validation(element_path, self.__value_type, value, results)
        else:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_ISNOT_MAP",
                    name + " type is expected to be Map",
                    "Map",
                    type(value)
                )
            )
