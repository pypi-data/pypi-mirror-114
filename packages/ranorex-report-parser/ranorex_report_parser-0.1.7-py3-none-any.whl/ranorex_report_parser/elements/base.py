from typing import List, Union
from datetime import datetime, timedelta

from enum import Enum

class ReportStatus(Enum):
    Success = 1
    Failed = 2
    Ignored = 3

class ReportElement(object):
    def __init__(self, start_time: datetime, duration: int):
        self.start_time = start_time
        self.duration = duration

        self._order = []

    def add_element(self, element: 'ReportElement'):
        self._order.append(element)

    def get_order(self) -> List['ReportElement']:
        """
        Return the order of all child elements of this element
        """
        return list(self._order) # Return new object instead of reference to _order

    def get_full_order(self) -> List['ReportElement']:
        """
        Returns the order including all subchildren of the element, including iteself.
        """
        order = [self]
        for element in self.get_order():
            order += element.get_full_order()

        return order

    def parse_attributes(self, attribs: dict):
        raise NotImplementedError(f"Method is not implemented for class {self.__class__}")

    def sync_start_time(self):
        assert self.start_time is not None, "Cannot sync time when parent has not start time"
        
        start_time = self.start_time
        for element in self.get_order():
            if element.start_time is None:
                element.start_time = start_time ## do not override time already inputted
            start_time += timedelta(milliseconds=element.duration)

            element.sync_start_time() ## recursively sync time

class ReportElementWithStatus(ReportElement):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus):
        super().__init__(start_time, duration)

        self.status = status

