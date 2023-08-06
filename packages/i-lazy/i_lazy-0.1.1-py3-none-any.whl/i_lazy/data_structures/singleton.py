from typing import Any, Dict, Generic, Optional, Tuple, Type, TypeVar

T = TypeVar("T", bound="Singleton")


class Singleton(Generic[T]):

    _instance: Optional[T] = None

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance
        return cls._instance


U = TypeVar("U", bound="SingletonMeta")


class SingletonMeta(type, Generic[U]):

    def __init__(self: U, name: str, bases: Tuple[type, ...], dict_: Dict[str, Any], **kwargs) -> None:
        self._instance: Optional[U] = None
        type.__init__(self, name, bases, dict_, **kwargs)

    def __call__(self: U, *args: Any, **kwargs: Any) -> U:
        """ From: https://docs.python.org/3/reference/datamodel.html
            3.3.6. Emulating callable objects
            object.__call__(self[, args...])
            Called when the instance is "called" as a function; if this method is defined, 
            x(arg1, arg2, ...) roughly translates to type(x).__call__(x, arg1, ...).
        """
        if self._instance is None:
            # type(x)(...) does not expand to type.__call__(x, ...) [or, equivalently, type(x).__call__(x, ...)], probably cuz of C binding
            self._instance = type.__call__(self, *args, **kwargs)
            return self._instance
        else:
            return self._instance
