from typing import Any, NamedTuple, Optional, Type, Union

from .field import Field


class FieldInfo(NamedTuple):
    name_to_set: str
    obj: Field


class SubConfigInfo(NamedTuple):
    name_to_set: str
    obj: type


def is_dunder(name: str) -> bool:
    if name.startswith("__") and name.endswith("__"):
        return True
    else:
        return False


def parse_objects(
        obj_to_parse: Union[Type["Config"], "Config"]
) -> list[Union[FieldInfo, SubConfigInfo]]:
    result = []
    for var in dir(obj_to_parse):
        name_to_set = var
        if is_dunder(name_to_set):
            continue
        obj: Any = getattr(obj_to_parse, var)
        if isinstance(obj, Field):
            result.append(FieldInfo(name_to_set=name_to_set, obj=obj))
        elif type(obj) is type:
            result.append(SubConfigInfo(name_to_set=name_to_set, obj=obj))
    return result


class Config:
    _prefix_: Optional[str] = None

    def __init__(self, **to_override):
        self._init_fields(self._prefix_, self, **to_override)

    @classmethod
    def _init_fields(
            cls, path: str, config: Union["Config", type], **to_override
    ):
        """
        Put the value in the configs
        :param path: path to config
        :param config:
        :return:
        """
        config = config() if type(config) is type else config
        path = f"{path}." if path else ""
        result = parse_objects(config)
        for obj in result:
            if obj.name_to_set in to_override:
                setattr(config, obj.name_to_set, to_override.get(obj.name_to_set))
            elif isinstance(obj, SubConfigInfo):
                _path = f"{path}{obj.name_to_set}".replace(".", "_").upper()
                sub_config = cls._init_fields(_path, obj.obj)
                setattr(config, obj.name_to_set, sub_config)
            else:
                if obj.obj.name is None:
                    obj.obj.name = f"{path}{obj.name_to_set}".replace(".", "_").upper()
                setattr(config, obj.name_to_set, obj.obj.value)
        return config

    def as_dict(self):
        return as_dict(self)


def as_dict(cfg: Union["Config", type]) -> dict:
    """
    config serialization
    :param cfg:
    :return:
    """
    result = dict()
    for i_name in dir(cfg):
        if is_dunder(i_name):
            continue
        i_var = getattr(cfg, i_name)
        if callable(i_var):
            continue
        if hasattr(i_var, "__dict__"):
            result[i_name] = as_dict(i_var)
            continue
        result[i_name] = i_var
    return result
