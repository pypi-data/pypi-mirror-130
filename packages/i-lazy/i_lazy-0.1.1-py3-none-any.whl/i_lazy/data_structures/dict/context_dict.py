from pprint import pformat
from typing import (Any, Callable, Dict, Iterable, Iterator, List, Mapping,
                    Tuple, Type, TypeVar, Union)

from i_lazy.utils.dict import path_get
from i_lazy.utils.type_ocd import ListOr, list_or, validate_or

Index = Union[str, int]
KT = TypeVar('KT')  # Key type.
VT = TypeVar('VT')  # Value type.
VT_co = TypeVar('VT_co', covariant=True)


class ContextDictError(Exception):

    def __init__(self, msg: str, context: "FrozenContextDict", *args: Any) -> None:
        self.msg = msg
        self.context = context
        super().__init__(msg, context, *args)

    def __repr__(self) -> str:
        return self.msg + "\nContext:\n" + pformat(self.context.context)


class FrozenContextDict(Mapping[KT, VT]):

    __slots__ = ["_context", "_path"]

    def __init__(self, context: Dict[KT, VT], path: Iterable[KT]) -> None:
        self._context = context
        self._path: Tuple[KT, ...] = tuple(path)
        self._current = path_get(self._context, self._path)
        super().__init__()

    def __getitem__(self, key: KT) -> VT:
        return self._current[key]

    def __len__(self) -> int:
        return len(self._current)

    def __iter__(self) -> Iterator[KT]:
        return iter(self._current)

    def __repr__(self) -> str:
        return repr(self._current)

    @property
    def context(self) -> Dict[KT, VT]:
        return self._context

    @property
    def path(self) -> Tuple[KT, ...]:
        return self._path

    @property
    def current(self) -> Dict[KT, VT]:
        return self._current

    def validate(self, key: KT, validator: Union[Type[VT], Callable[[VT], bool]], default: Union[None, VT, Callable[..., VT]]) -> VT:
        full_path: List[Any] = [*self.path, key]
        full_path_str = '.'.join(full_path)
        # If key exists
        if key in self:
            val = self[key]
            # Validate by type
            if validate_or(val, validator):
                return val
            else:
                raise ContextDictError(
                    f"Invalid value at {full_path_str}", self)
        # If key does not exist
        elif default is None:
            raise ContextDictError(f"Missing value at {full_path_str}", self)

        if callable(default):
            return default()

        return default

    def move(self, steps: ListOr[KT]) -> "FrozenContextDict[Any, Any]":
        return FrozenContextDict(self.context, [*self.path, *list_or(steps)])


class ContextDict(FrozenContextDict[KT, VT]):

    __slots__ = ["_context", "_path"]

    def __setitem__(self, key: KT, val: VT) -> None:
        self._current[key] = val

    def __delitem__(self, key: KT) -> None:
        del self._current[key]
