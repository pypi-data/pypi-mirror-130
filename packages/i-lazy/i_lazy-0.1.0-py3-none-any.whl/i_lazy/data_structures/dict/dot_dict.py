from typing import Generic, TypeVar

VT = TypeVar("VT")


class DotDict(dict, Generic[VT]):
    def __getattr__(self, key: str) -> VT:
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key: str, value: VT) -> None:
        self[key] = value

    def __delattr__(self, key: str):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)
