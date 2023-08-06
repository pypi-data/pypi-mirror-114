from datetime import datetime

from .base import ReportElementWithStatus, ReportStatus
from .test_module import TestModuleElement

class ModuleGroupElement(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus, display_name: str):
        super().__init__(start_time, duration, status)

        self.display_name = display_name

        self._test_modules = []

    def __str__(self):
        return f'<ModuleGroupElement display_name: "{self.display_name}" status: {self.status}>'

    def add_test_module(self, test_module: TestModuleElement):
        self.add_element(test_module)
        self._test_modules.append(test_module)