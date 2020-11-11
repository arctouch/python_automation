import json
import re

from appium.webdriver.common.mobileby import MobileBy as By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import support.constants.wait_time as wait
from support.locators import Element, Locator


def _name_of_page(page):
    return re.sub(r"Page$", "", type(page).__name__)


class ElementNotFoundException(Exception):
    pass


class BasePage:
    """Base class for all pages classes

    This class creates the necessary variables that a page objects needs to
    work, and so, it must be inherithed by all of them.

    While this class doesn't deliver any callable methods by the user, it does
    for the elements classes, which execute methods defined here on their
    execution.
    """

    def __init__(self, context):
        self.context = context
        self.driver = context.runner.driver
        self.platform = context.runner.platform
        self.locators = {
            value: value.locator for name, value in vars(type(self)).items() if
            not name.startswith('_') and name.isupper() and type(value) is Element
        }

    # IDENTITY AND NAVIGATION ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def name(self):
        return _name_of_page(self)

    @property
    def trait(self) -> Element:
        raise Exception("'trait' property must be overridden")

    @property
    def locators_description(self):
        formatted = {element.identity: locator.__repr__() for element, locator in self.locators.items()}
        return formatted

    @property
    def is_current_page(self):
        return self.wait_to_be_current_page(wait_time=wait.SHORT_WAIT)

    def wait_to_be_current_page(self, wait_time=wait.SHORT_WAIT):
        element = self.find_or_none(self.trait, wait_time=wait_time)
        return element.is_displayed() if element is not None else False

    @property
    def previous_screen(self):
        return None

    @property
    def path_switcher(self):
        raise Exception("path_switcher not defined in '{}'".format(self))

    def navigate(self):
        assert not self.is_current_page, "'{}' is the current page".format(self.name)

        if self.previous_screen is not None:
            self.previous_screen.navigate_to(self)

        assert self.is_current_page, "'{}' is not the current page".format(self.name)
        return self

    def navigate_to(self, page):
        if not self.is_current_page:
            self.navigate()

        execute_path = self.path_switcher.get(type(page), None)
        assert execute_path, \
            "Path not found: '{}' => '{}'".format(self, page)

        execute_path()
        assert page.wait_to_be_current_page(), \
            "Failed to navigate: '{}' => '{}'".format(self, page)

        return page

    # ELEMENTS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __get_element(self, locator, wait_time):
        """Searches for an appium/selenium element
        This method tries to search for an element with the specified query
        (element querry) using the specified way to search it (by). Also, if a
        'wait_time' is specified, it will wait that long before returning a
        'NoSuchElementException' exception.
        """
        query = locator.query(self.context.runner.platform)
        if wait_time and wait_time > 0:
            el = WebDriverWait(self.driver, wait_time, 0, TimeoutException).until(
                EC.presence_of_element_located(query))
        else:
            el = self.driver.find_element(*query)
        return el

    def __get_elements(self, locator, wait_time):
        """Searches for an appium/selenium element
        This method searches for elements matching the specified query
        (element querry) using the specified way to search it (by). Also, if a
        'wait_time' is specified, it will wait that long before returning a
        'NoSuchElementException' exception.
        """
        query = locator.query(self.platform)
        if wait_time and wait_time > 0:
            els = WebDriverWait(self.driver, wait_time, 0, TimeoutException).until(
                EC.presence_of_all_elements_located(query))
        else:
            els = self.driver.find_elements(*query)
        return els

    def __get_locator(self, element):
        """Searches for a locator tuple in the specified dict
        This method receives a dict of tuples, and the name of the wanted
        element. Then it tries to find a locator with that name, and if found,
        the same is returned.
        """
        assert element in self.locators, "Element '{}' doesn't exist in: '{}'\nLocators = {}" \
            .format(element.identity, self, json.dumps(self.locators_description, indent=2, sort_keys=True))

        return self.locators[element]

    def find_or_none(self, element, wait_time=0):
        return self.find(element, wait_time, should_fail=False)

    def find(self, element, wait_time=0, should_fail=True):
        el_locator = self.__get_locator(element)
        try:
            el = self.__get_element(el_locator, wait_time)
        except (TimeoutException, NoSuchElementException):
            el = None

        if should_fail:
            assert el, "Element not found: {element}\nPage: '{page}'\nWait time: {timeout}\n{locator}" \
                .format(element=element.identity, page=self.name, locator=el_locator, timeout=wait_time)

        return el

    # ELEMENT STATE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def tap_cell_at_position(self, position, wait_time=0):
        element = Element.cell(position=position)
        el_locator = Locator(
            ios=(By.IOS_CLASS_CHAIN, '**/XCUIElementTypeCell[{index}]'
                 .format(index=position)),
            android=(By.NAME, 'new UiSelector().className(“android.widget.LinearLayout”).index({index})'
                     .format(index=position))
        )

        try:
            cell = self.__get_element(el_locator, wait_time)
            cell.click()
        except (TimeoutException, NoSuchElementException):
            message = "Element not found: {element}\nPage: '{page}'\nWait time: {timeout}\n{locator}" \
                .format(element=element, page=self.name, locator=el_locator, timeout=wait_time)

            raise ElementNotFoundException(message)

    def element_is_disabled(self, element, wait_time=0):
        return not self.find(element, wait_time).is_enabled()

    def element_is_enabled(self, element, wait_time=0):
        return self.find(element, wait_time).is_enabled()

    def element_is_checked(self, element, wait_time=0):
        return self.find(element, wait_time).get_attribute('checked')

    def element_is_displayed(self, element, wait_time=0):
        return self.find(element, wait_time).is_displayed()

    def element_is_not_displayed(self, element, wait_time=0):
        return not self.element_is_displayed(element, wait_time)

    # INTERACTION ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def text_of_element(self, element, wait_time=0):
        return self.find(element, wait_time).text

    def send_value(self, element, value, wait_time=0):
        self.find(element, wait_time).send_keys(value)

    def tap_element(self, element, wait_time=0):
        element = self.find(element, wait_time)
        assert element.is_displayed(), "'{}' is not displayed"
        element.click()
