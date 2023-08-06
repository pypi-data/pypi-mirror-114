from datetime import datetime
from typing import Union

from .base import ReportStatus, ReportElementWithStatus
from .test_case import TestCaseElement
from .smart_folder import SmartFolderElement

class IterationContainerElement(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus):
        super().__init__(start_time, duration, status)

        self.data_source = ""

        self._iterations = []

    def add_iteration(self, iteration: Union[SmartFolderElement, TestCaseElement]):
        self.add_element(iteration)
        self._iterations.append(iteration)

    def parse_attributes(self, attribs: dict):
        self.data_source = attribs.get('datasource', '')