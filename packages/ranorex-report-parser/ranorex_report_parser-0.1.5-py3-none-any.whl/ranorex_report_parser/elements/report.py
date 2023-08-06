from datetime import datetime
from typing import List

from .base import ReportElementWithStatus, ReportStatus, ReportElement
from .test_suite import TestSuiteElement
from .test_case import TestCaseElement
from .test_module import TestModuleElement

class RootElement(ReportElementWithStatus):
    def __init__(self, start_time: datetime, duration: int, status: ReportStatus):
        super().__init__(start_time, duration, status)

        self.id = ""
        self.user = ""
        self.host = ""
        self.ranorex_version = ""
        self.os_version = ""
        self.runtime_version = ""
        self.processor_arch = ""
        self.screen_resolution = ""

        self._test_suite = None

    def set_test_suite(self, test_suite: TestSuiteElement):
        self._test_suite = test_suite

    def get_order(self):
        if self._test_suite:
            return [self._test_suite]
        return []

    def parse_attributes(self, attribs: dict):
        self.user = attribs.get('user', '')
        self.host = attribs.get('host', '')
        self.ranorex_version = attribs.get('rxversion', '')
        self.os_version = attribs.get('osversion', '')
        self.runtime_version = attribs.get('runtimeversion', '')
        self.processor_arch = attribs.get('procarch', '')
        self.screen_resolution = attribs.get('screenresolution', '')

        id = attribs.get('rid')
        timestamp = int(datetime.fromisoformat(attribs['timestampiso']).timestamp())
        self.id = f"{id}_{self.host}_{timestamp}"

class RanorexReport(ReportElement):
    def __init__(self, root: RootElement):
        super().__init__(root.start_time, root.duration)
        
        self._root = root
        self.add_element(root)

    def get_test_cases_by_name(self, display_name: str) -> List[TestCaseElement]:
        def test_case_filter(element: ReportElement):
            if isinstance(element, TestCaseElement):
                if element.display_name == display_name:
                    return True
            return False

        return list(filter(test_case_filter, self.get_full_order()))

    def has_testsuite(self) -> bool:
        return self._root._test_suite is not None

    def generate_meta_data(self) -> dict:
        meta_data = {}

        if self._root:
            meta_data['start_time'] = self._root.start_time
            meta_data['duration'] = self._root.duration ## This is unreliable, will be replaced by value in testsuite if that exists
            meta_data['id'] = self._root.id
            meta_data['host'] = self._root.host
            meta_data['user'] = self._root.user
            meta_data['os_version'] = self._root.os_version
            meta_data['ranorex_version'] = self._root.ranorex_version
            meta_data['runtime_version'] = self._root.runtime_version
            meta_data['processor_arch'] = self._root.processor_arch
            meta_data['screen_resolution'] = self._root.screen_resolution
        if self.has_testsuite():
            meta_data['duration'] = self._root._test_suite.duration
            meta_data['display_name'] = self._root._test_suite.display_name
            meta_data['run_configuration'] = self._root._test_suite.run_config

        return meta_data

    def get_test_suite(self) -> TestSuiteElement:
        return self._root._test_suite

    def get_test_cases(self) -> List[TestCaseElement]:
        return list(filter(lambda e: isinstance(e, TestCaseElement), self.get_full_order()))

    def get_test_modules(self) -> List[TestModuleElement]:
        return list(filter(lambda e: isinstance(e, TestModuleElement), self.get_full_order()))
