"""
Hossein Moein
February 8, 2019
Copyright (C) 2019-2020 Hossein Moein
Distributed under the BSD Software License (see file LICENSE)
"""

from datetime import datetime
from typing import TypeVar, Union

from .data_item_base import AllowedBaseTypes, DataItemBase


_DataItemType = TypeVar('_DataItemType', bound='DataItem')


class DataItem(DataItemBase):
    """A concrete data item with actual value."""

    def __init__(self: _DataItemType, value: AllowedBaseTypes) -> None:
        """Initialize."""
        super().__init__()
        self._value: AllowedBaseTypes = value

    def get_value(self: _DataItemType) -> AllowedBaseTypes:
        """Get value method for DataItem."""
        return self._value

    def __eq__(self: _DataItemType, other: DataItemBase) -> bool:
        """== operator."""
        if not all([self._value, other.get_value()]):
            return True
        elif self._value is None or other.get_value() is None:
            return False
        lhs = self._value if not isinstance(self._value, datetime) else self._value.timestamp()
        rhs = ((type(self._value)(other.get_value()))
               if not isinstance(other.get_value(), datetime) else other.get_value().timestamp()
               )
        return lhs == rhs

    def __lt__(self: _DataItemType, other: DataItemBase) -> bool:
        """< operator."""
        if self._value is None or other.get_value() is None:
            return False
        lhs = self._value if not isinstance(self._value, datetime) else self._value.timestamp()
        rhs = ((type(self._value)(other.get_value()))
               if not isinstance(other.get_value(), datetime) else other.get_value().timestamp()
               )
        return lhs < rhs

    def __gt__(self: _DataItemType, other: DataItemBase) -> bool:
        """> operator."""
        if self._value is None or other.get_value() is None:
            return False
        lhs = self._value if not isinstance(self._value, datetime) else self._value.timestamp()
        rhs = ((type(self._value)(other.get_value()))
               if not isinstance(other.get_value(), datetime) else other.get_value().timestamp()
               )
        return lhs > rhs

    def _set_to_null_hook(self: _DataItemType) -> bool:
        """This is the only way to set an existing non-null DataItem to null"""
        if self._value is not None:
            self._value = None
            return True
        return False

    def _set_hook(self: _DataItemType, value: Union[DataItemBase, AllowedBaseTypes]) -> bool:
        """Set hook method."""
        value_to_set = type(self._value)(value) if self._value is not None else value
        # if nothing needs to be changed, return False so dependencies do not trigger
        if self._value == value_to_set:
            return False
        self._value = value_to_set
        return True