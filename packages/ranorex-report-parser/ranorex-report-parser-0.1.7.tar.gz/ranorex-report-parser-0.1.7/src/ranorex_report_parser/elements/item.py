from datetime import datetime

from .base import ReportElement


class ItemElement(ReportElement):
    def __init__(self, start_time: datetime, duration: int, message: str):
        super().__init__(start_time, duration)

        self.message = message

    def __str__(self):
        return f'<ItemElement message: "{self.message}">'
