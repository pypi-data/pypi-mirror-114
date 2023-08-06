from typing import Union

from datetime import datetime, timedelta
from logging import getLogger
from typing import IO, List
from xml.etree.ElementTree import ElementTree

import defusedxml.ElementTree as ET

from .elements import *

logger = getLogger()

DATE_FORMAT = r"%d/%m/%Y %I:%M:%S %p"
TIME_FORMAT = r"%M:%S.%f"

def parse(file: Union[IO, str]) -> RanorexReport:
    report = ET.parse(file).getroot()
    assert len(report) == 1, "Invalid report file"
    assert report.tag == 'report', "Invalid report file"

    return RanorexReport(parse_report(report))

def parse_report(report: ElementTree) -> RootElement:
    root = report.find("./activity[@type='root']")

    start_time = datetime.fromisoformat(root.attrib['timestampiso'])
    duration = int(root.attrib['durationms'])
    status = ReportStatus[root.attrib['result']]
    
    root_element = RootElement(start_time, duration, status)
    
    root_element.set_test_suite(parse_test_suite(root))
    root_element.sync_start_time()
    root_element.parse_attributes(root.attrib)

    return root_element

def parse_test_suite(root: ElementTree) -> TestSuiteElement:
    test_suite = root.find("./activity[@type='test-suite']")

    if test_suite is None:
        logger.error("Report does not have any valid test-suites")
        return None

    duration = int(test_suite.attrib['durationms'])
    status = ReportStatus[root.attrib['result']]
    display_name = test_suite.attrib['testsuitename']

    test_suite_element = TestSuiteElement(None, duration, status, display_name)
    test_suite_element.parse_attributes(test_suite.attrib)

    for activity in test_suite.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "setup-container":
            test_suite_element.set_setup(parse_setup_container(activity))
        elif activity_type == "test-case":
            test_suite_element.add_test_case(parse_test_case(activity))
        elif activity_type in ("smart-folder", "entry-container"):
            test_suite_element.add_smart_folder(parse_smart_folder(activity))
        elif activity_type == "iteration-container":
            test_suite_element.add_iteration_container(parse_iteration_container(activity))
        elif activity_type == "teardown-container":
            test_suite_element.set_teardown(parse_teardown_container(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing test suite")

    return test_suite_element

def parse_setup_container(setup: ElementTree) -> SetupContainerElement:
    duration = duration = int(setup.attrib['durationms'])
    status = ReportStatus[setup.attrib['result']]

    setup_element = SetupContainerElement(None, duration, status)
    setup_element.parse_attributes(setup.attrib)

    for activity in setup.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "test-module":
            setup_element.add_test_module(parse_test_module(activity))
        elif activity_type == "module-group":
            setup_element.add_module_group(parse_module_group(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing setup container")

    return setup_element

def parse_teardown_container(teardown: ElementTree) -> TeardownContainerElement:
    duration = duration = int(teardown.attrib['durationms'])
    status = ReportStatus[teardown.attrib['result']]

    teardown_element = TeardownContainerElement(None, duration, status)
    teardown_element.parse_attributes(teardown.attrib)
    

    for activity in teardown.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "test-module":
            teardown_element.add_test_module(parse_test_module(activity))
        elif activity_type == "module-group":
            teardown_element.add_module_group(parse_module_group(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing teardown container")

    return teardown_element

def parse_iteration_container(iteartion: ElementTree) -> IterationContainerElement:
    duration = duration = int(iteartion.attrib['durationms'])
    status = ReportStatus[iteartion.attrib['result']]

    iteration_element = IterationContainerElement(None, duration, status)
    iteration_element.parse_attributes(iteartion.attrib)

    for activity in iteartion.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "test-case":
            iteration_element.add_iteration(parse_test_case(activity))
        elif activity_type in ("smart-folder", "entry-container"):
            iteration_element.add_iteration(parse_smart_folder(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing iteration container")

    return iteration_element

def parse_test_case(test_case: ElementTree) -> TestCaseElement:
    duration = duration = int(test_case.attrib['durationms'])
    status = ReportStatus[test_case.attrib['result']]
    display_name = test_case.attrib['displayName']

    test_case_element = TestCaseElement(None, duration, status, display_name)
    test_case_element.parse_attributes(test_case.attrib)


    for activity in test_case.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "setup-container":
            test_case_element.set_setup(parse_setup_container(activity))
        elif activity_type == "test-module":
            test_case_element.add_test_module(parse_test_module(activity))
        elif activity_type == "iteration-container":
            test_case_element.add_iteration_container(parse_iteration_container(activity))
        elif activity_type == "module-group":
            test_case_element.add_module_group(parse_module_group(activity))
        elif activity_type in ("smart-folder", "entry-container"):
            test_case_element.add_smart_folder(parse_smart_folder(activity))
        elif activity_type == "teardown-container":
            test_case_element.set_teardown(parse_teardown_container(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing test case")

    return test_case_element

def parse_smart_folder(smart_folder: ElementTree) -> SmartFolderElement:
    duration = duration = int(smart_folder.attrib['durationms'])
    status = ReportStatus[smart_folder.attrib['result']]
    display_name = smart_folder.attrib['displayName']

    smart_folder_element = SmartFolderElement(None, duration, status, display_name)
    smart_folder_element.parse_attributes(smart_folder.attrib)

    for activity in smart_folder.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "setup-container":
            smart_folder_element.set_setup(parse_setup_container(activity))
        elif activity_type == "test-case":
            smart_folder_element.add_test_case(parse_test_case(activity))
        elif activity_type in ("smart-folder", "entry-container"):
            smart_folder_element.add_smart_folder(parse_smart_folder(activity))
        elif activity_type == "iteration-container":
            smart_folder_element.add_iteration_container(parse_iteration_container(activity))
        elif activity_type == "test-module":
            smart_folder_element.add_test_module(parse_test_module(activity))
        elif activity_type == "module-group":
            smart_folder_element.add_module_group(parse_module_group(activity))
        elif activity_type == "teardown-container":
            smart_folder_element.set_teardown(parse_teardown_container(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing smart folder")

    return smart_folder_element

def parse_module_group(module_group: ElementTree) -> ModuleGroupElement:
    duration = duration = int(module_group.attrib['durationms'])
    status = ReportStatus[module_group.attrib['result']]
    display_name = module_group.attrib['modulegroupname']

    module_group_element = ModuleGroupElement(None, duration, status, display_name)

    for activity in module_group.findall("./activity"):
        activity_type = activity.attrib.get('type')
        if activity_type == "test-module":
            module_group_element.add_test_module(parse_test_module(activity))
        else:
            logger.error(f"Found unknown type {activity_type} parsing module group")

    return module_group_element

def parse_test_module(test_module: ElementTree) -> TestModuleElement:
    duration = duration = int(test_module.attrib['durationms'])
    status = ReportStatus[test_module.attrib['result']]
    display_name = test_module.attrib['displayName']

    test_module_element = TestModuleElement(None, duration, status, display_name)
    test_module_element.parse_attributes(test_module.attrib)

    items = test_module.findall("./item")
    if items:
        relative_times: List[int] = []
        item_elements: List[ItemElement] = []
        
        # For some reason ranorex reports use relative time for report items
        # Calculate relative times for each item to test module start
        # Then calculate the duration relative to the test module duration
        for item in items:
            relative_time = datetime.strptime(item.attrib['timeRelativeToTestModuleStartTime'], TIME_FORMAT)
            relative_time = timedelta(minutes=relative_time.minute, seconds=relative_time.second, microseconds=relative_time.microsecond)
            relative_time = int(relative_time.total_seconds()*1000) # convert to ms
            relative_times.append(relative_time)

            message = item.find('message').text.strip()

            item_elements.append(ItemElement(None, None, message))

        relative_times.append(duration) # Add duration of test module to end of list
        for i, item in enumerate(item_elements):
            # duration = relative_time[next item] - relative_time[current_item]
            # the final item will be the test module duration
            item_duration = relative_times[i+1] - relative_times[i]
            item.duration = item_duration

            test_module_element.add_item(item)

    return test_module_element
