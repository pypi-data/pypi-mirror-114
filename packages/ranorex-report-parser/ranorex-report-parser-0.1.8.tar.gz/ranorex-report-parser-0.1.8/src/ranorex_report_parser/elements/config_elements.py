from datetime import datetime
from hashlib import sha256
from typing import List

from .base import ReportElement, ReportElementWithStatus, ReportStatus
from .module_group import ModuleGroupElement
from .test_module import TestModuleElement


class ConfigContainerElement(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus):
        super().__init__(start_time, duration, status)

        self.id = ""

        self._test_modules = []
        self._module_groups = []

    def add_test_module(self, test_module: TestModuleElement):
        self.add_element(test_module)
        self._test_modules.append(test_module)

    def add_module_group(self, module_group: ModuleGroupElement):
        self.add_element(module_group)
        self._module_groups.append(module_group)

    def parse_attributes(self, attribs: dict):
        self.id = attribs['rid']

    def get_hash(self) -> str:
        data = f"{self.start_time.isoformat()}-{self.duration}-{self.status.name}-{self.id}".encode()
        return sha256(data).hexdigest()

class SetupContainerElement(ConfigContainerElement):
    pass

class TeardownContainerElement(ConfigContainerElement):
    pass

class ReportElementWithSetupTeardown(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus):
        super().__init__(start_time, duration, status)

        self.setup = None
        self.teardown = None

    def set_setup(self, setup: SetupContainerElement):
        self.setup = setup

    def set_teardown(self, teardown: TeardownContainerElement):
        self.teardown = teardown

    def get_order(self) -> List[ReportElement]:
        order = super().get_order()

        if self.setup:
            order.insert(0, self.setup)
        if self.teardown:
            order.append(self.teardown)

        return order

    def calculate_total_setup_duration(self):
        duration = 0
        for item in self.get_full_order():
            if isinstance(item, ReportElementWithSetupTeardown):
                if item.setup:
                    duration += item.setup.duration

        return duration

    def calculate_total_teardown_duration(self):
        duration = 0
        for item in self.get_full_order():
            if isinstance(item, ReportElementWithSetupTeardown):
                if item.teardown:
                    duration += item.teardown.duration

        return duration

    def calculate_duration_less_setup_and_teardown(self):
        return self.duration - self.calculate_total_setup_duration() - self.calculate_total_teardown_duration()

    def get_hash(self) -> str:
        data = super().get_hash()
        if self.setup:
            data += self.setup.get_hash()
        if self.teardown:
            data += self.teardown.get_hash()

        return sha256(data.encode()).hexdigest()
