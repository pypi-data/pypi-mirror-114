from datetime import datetime

from .base import ReportStatus
from .test_module import TestModuleElement
from .module_group import ModuleGroupElement
from .config_elements import ReportElementWithSetupTeardown

class TestCaseElement(ReportElementWithSetupTeardown):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus, display_name: str):
        super().__init__(start_time, duration, status)

        self.display_name = display_name

        self.id = ""

        self._iteration_cointainers = []
        self._test_modules = []
        self._module_groups = []
        self._smart_folders = []

    def __str__(self):
        return f'<TestCaseElement display_name: "{self.display_name}" status: {self.status}>'

    def add_iteration_container(self, iteration_container: 'IterationContainerElement'):
        self.add_element(iteration_container)
        self._iteration_cointainers.append(iteration_container)

    def add_test_module(self, test_module: TestModuleElement):
        self.add_element(test_module)
        self._test_modules.append(test_module)

    def add_module_group(self, module_group: ModuleGroupElement):
        self.add_element(module_group)
        self._module_groups.append(module_group)
    
    def add_smart_folder(self, smart_folder: 'SmartFolderElement'):
        self.add_element(smart_folder)
        self._smart_folders.append(smart_folder)

    def parse_attributes(self, attribs: dict):
        self.id = attribs['testcontainerid']
