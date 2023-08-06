from functools import partial
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union

T = TypeVar("T")

# ---------------------------------------------------------------------------- #
#                                  Type Morphs                                 #
# ---------------------------------------------------------------------------- #

ListOr = Union[T, List[T]]


def list_or(obj: ListOr[T]) -> List[T]:
    """
    Takes in an item or a list of obj and returns a list of item(s).
    """

    if isinstance(obj, list):
        return obj
    else:
        return [obj]


def split_or(obj: Union[str, List[str]], delimiter: str = "\n") -> List[str]:
    """
    Takes in a string or a list of strings. Split string by delimiter to return a list of strings.
    """

    return obj.split(delimiter) if not isinstance(obj, list) else obj


def join_or(obj: Union[str, List[str]], delimiter: str = "\n") -> str:
    """
    Takes in a string or a list of strings. Join strings by delimiter to return a string.
    """

    return delimiter.join(obj) if isinstance(obj, list) else obj


def sure(obj: Optional[T]) -> T:
    """
    When you are sure that an object will not have None value.
    """
    assert obj is not None, "You promised it won't be null!"
    return obj

# ---------------------------------------------------------------------------- #
#                                  Type Checks                                 #
# ---------------------------------------------------------------------------- #


isint = partial(isinstance, __class_or_tuple=int)
isfloat = partial(isinstance, __class_or_tuple=float)
isstr = partial(isinstance, __class_or_tuple=str)
istuple = partial(isinstance, __class_or_tuple=tuple)
islist = partial(isinstance, __class_or_tuple=list)
isdict = partial(isinstance, __class_or_tuple=dict)
istype = partial(isinstance, __class_or_tuple=type)


def listinstance(obj: Any, type_: Type[T]) -> Tuple[bool, List[T]]:
    """
    Checks if an object is a list of the same given type. Returns check result and typed variable.

    Args:
        obj (Any): object to be checked.
        type_ (Type[T]): type to be checked against.

    Returns:
        Tuple[bool, List[T]]: check result, typed item.
    """
    if not isinstance(obj, list):
        return False, []
    if not all([isinstance(item, type_) for item in obj]):
        return False, []
    return True, obj


def validate_or(obj: T, validator: Union[Type[T], Callable[[T], bool]]) -> bool:
    return (isinstance(validator, type) and isinstance(obj, validator)) or (not isinstance(validator, type) and validator(obj))
