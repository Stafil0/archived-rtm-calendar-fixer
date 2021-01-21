# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

import json
from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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

    @staticmethod
    def from_dict(obj: Any) -> 'ICal':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("uri"))
        save = from_str(obj.get("save"))
        return ICal(uri, save)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uri"] = from_str(self.uri)
        result["save"] = from_str(self.save)
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
