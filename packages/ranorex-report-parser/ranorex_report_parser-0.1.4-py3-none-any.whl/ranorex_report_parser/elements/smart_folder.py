from datetime import datetime

from .base import ReportStatus
from .test_module import TestModuleElement
from .module_group import ModuleGroupElement
from .config_elements import ReportElementWithSetupTeardown

class SmartFolderElement(ReportElementWithSetupTeardown):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus, display_name: str):
        super().__init__(start_time, duration, status)

        self.display_name = display_name

        self.id = ""

        self._test_cases = []
        self._smart_folders = []
        self._iteration_containers = []
        self._module_groups = []
        self._test_modules = []

    def add_test_case(self, test_case: 'TestCaseElement'):
        self.add_element(test_case)
        self._test_cases.append(test_case)

    def add_smart_folder(self, smart_folder: 'SmartFolderElement'):
        self.add_element(smart_folder)
        self._smart_folders.append(smart_folder)
    
    def add_iteration_container(self, iteration_container: 'IterationContainerElement'):
        self.add_element(iteration_container)
        self._iteration_containers.append(iteration_container)

    def add_test_module(self, test_module: TestModuleElement):
        self.add_element(test_module)
        self._test_modules.append(test_module)

    def add_module_group(self, module_group: ModuleGroupElement):
        self.add_element(module_group)
        self._module_groups.append(module_group)

    def parse_attributes(self, attribs: dict):
        self.id = attribs['testcontainerid']