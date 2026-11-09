"""
A thin layer on top of pyads for some extra functionality.
"""

from typing import Any

from pyads import AdsSymbol

NestedSymbol = AdsSymbol  # Create an alias just so we can be sure our injection worked


def magic_getter(self: NestedSymbol, name: str) -> Any:
    """__getattr__ fallback-getter that we inject into the symbol class."""
    assert self.name is not None
    child_name = self.name + "." + name
    return self._plc.get_symbol(child_name)


NestedSymbol.__getattr__ = magic_getter
