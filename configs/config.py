# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

import json
from dataclasses import dataclass
from typing import Any, List

from configs.base import from_list, to_class
from configs.sections import FixSection, MergeSection


@dataclass
class Config:
    fix: List[FixSection]
    merge: List[MergeSection]

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        fix = from_list(FixSection.from_dict, obj.get("fix"))
        merge = from_list(MergeSection.from_dict, obj.get("merge"))
        return Config(fix, merge)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fix"] = from_list(lambda x: to_class(FixSection, x), self.fix)
        result["merge"] = from_list(lambda x: to_class(MergeSection, x), self.merge)
        return result


def read_config(path: Any) -> Config:
    with open(path, 'r', encoding='utf8') as f:
        return Config.from_dict(json.load(f))
