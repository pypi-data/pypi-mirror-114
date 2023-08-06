from datetime import datetime

from .base import ReportElementWithStatus, ReportStatus
from .item import ItemElement

class TestModuleElement(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus, display_name: str):
        super().__init__(start_time, duration, status)

        self.display_name = display_name

        self.id = ""
        self.module_type = ""

        self._items = []

    def __str__(self):
        return f'<TestModuleElement display_name: "{self.display_name}" status: {self.status}>'

    def add_item(self, item: ItemElement):
        self.add_element(item)
        self._items.append(item)

    def parse_attributes(self, attribs: dict):
        self.id = attribs['moduleid']
        self.module_type = attribs['moduletype']
