__all__ = ("PANDAS_AVAILABLE",)

from pkg_resources import working_set

from analytix.errors import MissingOptionalComponents

_packages = [p.key for p in working_set]
PANDAS_AVAILABLE = "pandas" in _packages
