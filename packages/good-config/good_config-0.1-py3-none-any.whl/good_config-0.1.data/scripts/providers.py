import os
from typing import Any


class AbstractProvider:
    """Implement this class and pass to `field`"""

    def get(self, name: str) -> Any:
        """Return a value or None"""
        raise NotImplementedError()


class EnvironmentProvider(AbstractProvider):
    """Default provider. Gets vals from environment"""

    def get(self, name: str) -> Any:
        return os.getenv(name)


DEFAULT_PROVIDER = EnvironmentProvider()
