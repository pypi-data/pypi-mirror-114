import logging
import typing

from .exceptions import ImpossibleToCastError


VT = typing.TypeVar('VT')


class AbstractCaster:
    def cast(self, val: str) -> typing.Union[typing.Any, typing.NoReturn]:
        """Try to cast or return val"""
        raise NotImplementedError()


class ConstantCaster(AbstractCaster, typing.Generic[VT]):
    ABLE_TO_CAST: typing.Dict[
        str, typing.Any
    ] = {}

    def cast(self, val: str) -> typing.Union[VT, typing.NoReturn]:
        """Cast using ABLE_TO_CAST dictionary as in BoolCaster"""
        if val.lower() in self.ABLE_TO_CAST:
            converted = self.ABLE_TO_CAST.get(val.lower())
            return typing.cast(VT, converted)

        raise ImpossibleToCastError(val, self)


class BoolCaster(ConstantCaster):
    ABLE_TO_CAST = {
        'true': True,
        '1': True,
        'yes': True,
        'ok': True,
        'on': True,
        'false': False,
        '0': False,
        'no': False,
        'off': False,
    }


class IntCaster(AbstractCaster):
    def cast(self, val: str) -> typing.Union[int, typing.NoReturn]:
        try:
            as_int = int(val)
            return as_int
        except ValueError:
            raise ImpossibleToCastError(val, self)


class FloatCaster(AbstractCaster):
    def cast(self, val: str) -> typing.Union[float, typing.NoReturn]:
        val = val.replace(',', '.')
        try:
            as_float = float(val)
            return as_float
        except ValueError:
            raise ImpossibleToCastError(val, self)


class ListCaster(AbstractCaster):
    def __init__(self, separator: str = ','):
        self.separator = separator

    def cast(self, val: str) -> typing.List[typing.Any]:
        if val.endswith(self.separator):
            val = val[0: len(val) - len(self.separator)]
        return val.split(self.separator)


class LoggingLogLevelCaster(ConstantCaster):
    ABLE_TO_CAST = {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARN,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }


class LoguruLogLevelCaster(ConstantCaster):
    levels = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    ABLE_TO_CAST = {level.lower(): level for level in levels}


class NothingCaster(AbstractCaster):
    """Caster who does nothing"""

    def cast(self, val: str) -> str:
        return val


DEFAULT_CASTER = NothingCaster()

__all__ = (
    'BoolCaster',
    'IntCaster',
    'FloatCaster',
    'ListCaster',
    'LoggingLogLevelCaster',
    'LoguruLogLevelCaster',
    'AbstractCaster',
    'ConstantCaster',
    'DEFAULT_CASTER',
)
