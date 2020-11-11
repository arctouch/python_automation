from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.webdriver.common.by import By as SeleniumBy

# It's importing the constants file
# import support.constants.Element.Kind as Element.Kind
# It's importing the way to search elements through ANDROID_UIAUTOMATOR
# It's importing the BasePage class, who has all the definitions that are using the Appium driver.
from selenium.webdriver.common.keys import Keys

from support.android.ui_automator import select_button_with_text, select_edit_text, get_description
from support.locators import Element, Locator
from support.model.user import User
from support.pages.base import BasePage


class LoginPage(BasePage):
    LOGIN_BUTTON = Element.button(
        name='Login',
        ios_query=(AppiumBy.ID, 'test-LOGIN'),
        android_query=(AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN'),
        web_query=(SeleniumBy.XPATH, '/html/body/div[2]/header')
    )

    USERNAME_INPUT = Element.input(
        name='Username',
        ios_query=(AppiumBy.ACCESSIBILITY_ID, 'test-Username'),
        android_query=(AppiumBy.ANDROID_UIAUTOMATOR, get_description('test-Username')),
        web_query=(SeleniumBy.XPATH, '/html/body/div[2]/header')
    )

    PASSWORD_INPUT = Element.input(
        name='Password',
        ios_query=(AppiumBy.ACCESSIBILITY_ID, 'test-Password'),
        android_query=(AppiumBy.ANDROID_UIAUTOMATOR, get_description('test-Password')),
        web_query=(SeleniumBy.XPATH, '/html/body/div[2]/header')
    )

    def __init__(self, context):
        super().__init__(context)

    @property
    def previous_screen(self):
        return None

    @property
    def trait(self) -> Element:
        return self.LOGIN_BUTTON

    @property
    def path_switcher(self):
        from pages import HomePage

        paths = {
            HomePage: self.log_in_default_user
        }

        return paths

    def tap_username(self):
        self.tap_element(self.USERNAME_INPUT)

    def tap_password(self):
        self.tap_element(self.PASSWORD_INPUT)

    def tap_login(self):
        self.tap_element(self.LOGIN_BUTTON)

    def type_credentials(self, user: User):
        self.send_value(self.USERNAME_INPUT, user.username)
        self.send_value(self.PASSWORD_INPUT, user.password)

    def log_in(self, user):
        self.type_credentials(user)
        self.tap_login()

    def log_in_default_user(self):
        self.log_in(self.context.user)
