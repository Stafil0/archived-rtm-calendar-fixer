from dataclasses import dataclass
from typing import Any, Optional

from base.calendar import Calendar
from configs.base import from_str, from_union, from_bool, from_none, to_enum


@dataclass
class ICalSection:
    uri: str
    timezone: str
    typo: Calendar
    with_estimate: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ICalSection':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("uri"))
        timezone = from_str(obj.get("timezone"))
        typo = Calendar(obj.get("typo"))
        with_estimate = from_union([from_bool, from_none], obj.get("with_estimate"))
        return ICalSection(uri, timezone, typo, with_estimate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uri"] = from_str(self.uri)
        result["timezone"] = from_str(self.timezone)
        result["typo"] = to_enum(Calendar, self.typo)
        result["with_estimate"] = from_union([from_bool, from_none], self.with_estimate)
        return result
