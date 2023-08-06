from dataclasses import dataclass, field
from typing import Any, Callable, Generic, List, Tuple, Type, TypeVar, Union

from i_lazy.data_structures.dict.context_dict import (ContextDict,
                                                      ContextDictError)

T = TypeVar("T")

Validator = Union[Type[T], Callable[[T], bool]]
DefaultOr = Union[None, T, Callable[..., T]]


@dataclass
class ValidationSpec(Generic[T]):
    key: T
    validator: Validator[T]
    default: DefaultOr[T]


SpecOr = Union[Tuple[T, Validator[T], DefaultOr[T]], ValidationSpec[T]]


def to_spec(spec: SpecOr[T]) -> ValidationSpec[T]:
    return spec if isinstance(spec, ValidationSpec) else ValidationSpec(*spec)


S = TypeVar("S", bound="DictSchema")


class DictSchemaError(Exception):

    def __init__(self, msg: str, context: "ContextDict", *args: Any) -> None:
        self.msg = msg
        self.context = context
        super().__init__(msg, context, *args)

    def __repr__(self) -> str:
        return self.msg


@dataclass
class DictSchema:

    checks: List[SpecOr] = field(default_factory=list)

    @classmethod
    def _from_dict(cls: Type[S], context: ContextDict) -> S:
        raise NotImplementedError(f"{cls.__name__}.from_dict not implemented")

    @classmethod
    def from_dict(cls: Type[S], context: ContextDict) -> S:
        try:
            for check in cls.checks:
                check_spec = to_spec(check)
                val = context.validate(
                    check_spec.key, check_spec.validator, check_spec.default)
                context[check_spec.key] = val
            instance: S = cls._from_dict(context)
        except ContextDictError as e:
            raise DictSchemaError(
                "Dictionary does not satisfy DictSchema\n" + e.msg, context)
        return instance
