# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Utility functions for the Oobeya library."""

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar, Union, get_args, get_origin

from dateutil import parser as date_parser

T = TypeVar("T")


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        snake_str: String in snake_case format

    Returns:
        String in camelCase format
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase to snake_case.

    Args:
        camel_str: String in camelCase format

    Returns:
        String in snake_case format
    """
    result = []
    for i, char in enumerate(camel_str):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def to_dict(obj: Any, convert_keys: bool = True) -> Any:
    """
    Convert a dataclass object to a dictionary with camelCase keys.

    Args:
        obj: Object to convert (typically a dataclass)
        convert_keys: Whether to convert snake_case keys to camelCase

    Returns:
        Dictionary representation of the object
    """
    if obj is None:
        return None

    if is_dataclass(obj) and not isinstance(obj, type):
        data = asdict(obj)
        if convert_keys:
            return {snake_to_camel(k): _convert_value(v) for k, v in data.items() if v is not None}
        return {k: _convert_value(v) for k, v in data.items() if v is not None}

    if isinstance(obj, dict):
        if convert_keys:
            return {snake_to_camel(k): _convert_value(v) for k, v in obj.items() if v is not None}
        return {k: _convert_value(v) for k, v in obj.items() if v is not None}

    if isinstance(obj, list):
        return [to_dict(item, convert_keys) for item in obj]

    return obj


def _convert_value(value: Any) -> Any:
    """Convert a value for JSON serialization."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return to_dict(value)
    if isinstance(value, dict):
        return {k: _convert_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_convert_value(item) for item in value]
    return value


def from_dict(data: Optional[Dict[str, Any]], cls: Type[T]) -> Optional[T]:
    """
    Convert a dictionary to a dataclass instance.

    Args:
        data: Dictionary to convert
        cls: Target dataclass type

    Returns:
        Instance of the dataclass or None if data is None
    """
    if data is None:
        return None

    if not is_dataclass(cls):
        return data  # type: ignore

    # Convert camelCase keys to snake_case
    converted_data: Dict[str, Any] = {}
    for key, value in data.items():
        snake_key = camel_to_snake(key)
        converted_data[snake_key] = value

    # Get type hints for the dataclass
    type_hints = cls.__annotations__

    # Process each field
    field_values: Dict[str, Any] = {}
    for field_name, field_type in type_hints.items():
        if field_name not in converted_data:
            continue

        value = converted_data[field_name]
        field_values[field_name] = _convert_field_value(value, field_type)

    return cls(**field_values)


def _convert_field_value(value: Any, field_type: Type[Any]) -> Any:
    """Convert a field value to the appropriate type."""
    if value is None:
        return None

    # Handle datetime fields
    if field_type is datetime:
        if isinstance(value, str):
            return date_parser.parse(value)
        return value

    # Handle list fields
    origin = get_origin(field_type)
    if origin is list:
        args = get_args(field_type)
        if args and isinstance(value, list):
            item_type = args[0]
            return [_convert_field_value(item, item_type) for item in value]
        return value

    # Handle dict fields
    if origin is dict:
        return value

    # Handle Optional/Union types
    if origin is Union:
        args = get_args(field_type)
        if len(args) >= 2 and type(None) in args:
            # This is Optional[T] - get the non-None type
            actual_type = args[0] if args[1] is type(None) else args[1]
            return _convert_field_value(value, actual_type)
        return value

    # Handle nested dataclasses
    if is_dataclass(field_type) and isinstance(value, dict):
        return from_dict(value, field_type)

    return value


def parse_datetime(date_string: Optional[str]) -> Optional[datetime]:
    """
    Parse a datetime string.

    Args:
        date_string: String to parse

    Returns:
        Datetime object or None if string is None or empty
    """
    if not date_string:
        return None
    try:
        return date_parser.parse(date_string)
    except (ValueError, TypeError):
        return None


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Format a datetime object to ISO format string.

    Args:
        dt: Datetime object to format

    Returns:
        ISO format string or None if dt is None
    """
    if dt is None:
        return None
    return dt.isoformat()


def build_query_params(**kwargs: Any) -> Dict[str, Any]:
    """
    Build query parameters, filtering out None values.

    Args:
        **kwargs: Query parameters

    Returns:
        Dictionary with non-None values
    """
    params: Dict[str, Any] = {}
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, list):
                # Handle list parameters
                params[key] = value
            elif isinstance(value, bool):
                # Convert bool to lowercase string for API
                params[key] = str(value).lower()
            else:
                params[key] = value
    return params
