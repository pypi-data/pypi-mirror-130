
from typing import Any, Dict, Iterable

from flatdict import FlatDict


def path_get(obj: Dict[Any, Any], path: Iterable[Any]) -> Any:
    curr = obj
    for step in path:
        curr = curr[step]
    return curr


def deep_merge(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge dictionaries by flattening.

    Args:
        dicts (List[Dict[str, Any]]): dictionaries to be merged.

    Returns:
        Dict[str, Any]: merged dictionary.
    """

    empty_dict: Dict[str, Any] = {}
    merged = FlatDict(empty_dict)
    for item in dicts:
        merged.update(FlatDict(item))
    return merged.as_dict()
