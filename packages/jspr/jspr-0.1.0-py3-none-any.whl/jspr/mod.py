from typing import Iterable, Mapping

from jspr.lang import raise_

from .runtime import Value


class Module:
    def __init__(self, name: str, items: Mapping[str, Value]) -> None:
        self._name = name
        self._items = dict(items)

    @property
    def name(self) -> str:
        """The name of the module"""
        return self._name

    def keys(self) -> Iterable[str]:
        """Get the names that are available in this module"""
        return self._items.keys()

    def __contains__(self, key: str) -> bool:
        return key in self._items

    def __jspr_getattr__(self, key: str) -> Value:
        try:
            return self._items[key]
        except KeyError:
            raise_(['mod-name-error', self.name, key])

    def __repr__(self) -> str:
        return f'<jspr.Module name="{self.name}">'
