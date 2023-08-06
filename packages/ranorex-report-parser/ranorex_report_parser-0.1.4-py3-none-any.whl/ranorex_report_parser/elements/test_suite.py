from datetime import datetime

from .base import ReportStatus
from .config_elements import ReportElementWithSetupTeardown
from .test_case import TestCaseElement
from .smart_folder import SmartFolderElement
from.iteration_container import IterationContainerElement

# Test Suites are essentially Smart Folders
class TestSuiteElement(ReportElementWithSetupTeardown):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus, display_name: str):
        super().__init__(start_time, duration, status)

        self.display_name = display_name

        self.id = ""
        self.run_config = ""

        self._test_cases = []
        self._smart_folders = []
        self._iteration_containers = []

    def add_test_case(self, test_case: TestCaseElement):
        self.add_element(test_case)
        self._test_cases.append(test_case)

    def add_smart_folder(self, smart_folder: SmartFolderElement):
        self.add_element(smart_folder)
        self._smart_folders.append(smart_folder)
    
    def add_iteration_container(self, iteration_container: IterationContainerElement):
        self.add_element(iteration_container)
        self._iteration_containers.append(iteration_container)

    def parse_attributes(self, attribs: dict):
        self.id = attribs['rid']
        self.run_config = attribs.get('runconfigname', "")
