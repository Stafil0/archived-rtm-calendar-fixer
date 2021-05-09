from dataclasses import dataclass
from typing import Any

from configs.sections.ical_section import ICalSection
from configs.base import from_str


@dataclass
class FixSection:
    calendar: ICalSection
    save: str

    @staticmethod
    def from_dict(obj: Any) -> 'FixSection':
        assert isinstance(obj, dict)
        calendar = ICalSection.from_dict(obj.get("calendar"))
        save = from_str(obj.get("save"))
        return FixSection(calendar, save)

    def to_dict(self) -> dict:
        result: dict = {}
        result["calendar"] = self.calendar.to_dict()
        result["save"] = from_str(self.save)
        return result
