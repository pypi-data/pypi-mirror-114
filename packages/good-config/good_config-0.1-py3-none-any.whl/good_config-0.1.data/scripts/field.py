from typing import Any, Optional

from .casters import AbstractCaster, DEFAULT_CASTER
from .exceptions import ImpossibleToCastError, VariableNotFoundError
from .providers import AbstractProvider, DEFAULT_PROVIDER

_NO_DEFAULT = object()


class Field:
    def __init__(
            self,
            name: Optional[str] = None,
            default: Optional[Any] = _NO_DEFAULT,
            provider: AbstractProvider = DEFAULT_PROVIDER,
            caster: AbstractCaster = DEFAULT_CASTER,
            ignore_caster_error: bool = False,
    ):
        self.name = name
        self._provider = provider
        self._value = None
        self._default = default
        self._caster = caster
        self._ignore_caster_error = ignore_caster_error

    @property
    def value(self):
        if self.name is None:
            raise VariableNotFoundError('No name')

        self._value = self.get_provider_value()

        if self._value is None:
            return self._get_default_value()

        return self._get_casted_value()

    def get_provider_value(self):
        return self._provider.get(self.name)

    def _get_default_value(self):
        if self._default is _NO_DEFAULT:
            raise VariableNotFoundError(self.name)

        if callable(self._default):
            return self._default()
        else:
            return self._default

    def _get_casted_value(self):
        try:
            casted = self._caster.cast(self._value)
        except ImpossibleToCastError as e:
            if self._ignore_caster_error:
                return e.val
            else:
                raise e

        else:
            return casted
