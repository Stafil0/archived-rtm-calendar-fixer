from dataclasses import dataclass
from typing import Any, List

from configs.sections.ical_section import ICalSection
from configs.base import from_str, from_list, to_class


@dataclass
class MergeSection:
    calendars: List[ICalSection]
    save: str

    @staticmethod
    def from_dict(obj: Any) -> 'MergeSection':
        assert isinstance(obj, dict)
        calendars = from_list(ICalSection.from_dict, obj.get("calendars"))
        save = from_str(obj.get("save"))
        return MergeSection(calendars, save)

    def to_dict(self) -> dict:
        result: dict = {}
        result["calendars"] = from_list(lambda x: to_class(ICalSection, x), self.calendars)
        result["save"] = from_str(self.save)
        return result
