# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

import json
from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, Optional, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ICal:
    uri: str
    save: str
    timezone: str
    with_estimate: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ICal':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("uri"))
        save = from_str(obj.get("save"))
        timezone = from_str(obj.get("timezone"))
        with_estimate = from_union([from_bool, from_none], obj.get("with_estimate"))
        return ICal(uri, save, timezone, with_estimate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uri"] = from_str(self.uri)
        result["save"] = from_str(self.save)
        result["timezone"] = from_str(self.timezone)
        result["with_estimate"] = from_union([from_bool, from_none], self.with_estimate)
        return result


@dataclass
class Config:
    events: List[ICal]
    tasks: List[ICal]

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        events = from_list(ICal.from_dict, obj.get("events"))
        tasks = from_list(ICal.from_dict, obj.get("tasks"))
        return Config(events, tasks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["events"] = from_list(lambda x: to_class(ICal, x), self.events)
        result["tasks"] = from_list(lambda x: to_class(ICal, x), self.tasks)
        return result


def read_config(path: Any) -> Config:
    with open(path, 'r', encoding='utf8') as f:
        return Config.from_dict(json.load(f))
