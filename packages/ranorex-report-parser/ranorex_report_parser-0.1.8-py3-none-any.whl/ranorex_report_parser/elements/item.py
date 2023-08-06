from datetime import datetime

from .base import ReportElement


class ItemElement(ReportElement):
    def __init__(self, start_time: datetime, duration: int, message: str, item_index: int = 0):
        super().__init__(start_time, duration)

        self.message = message
        self.category = ""
        self.item_index = item_index
        self.log_level = ""

    def __str__(self):
        return f'<ItemElement message: "{self.message}">'

    def parse_attributes(self, attribs: dict):
        self.log_level = attribs.get('level', '')
        self.category = attribs.get('category', '')
