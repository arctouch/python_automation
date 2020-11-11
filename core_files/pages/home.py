from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.webdriver.common.by import By as SeleniumBy

# It's importing the constants file
# It's importing the way to search elements through ANDROID_UIAUTOMATOR
from support.android.ui_automator import get_text, get_description
# It's importing the BasePage class, who has all the definitions that are using the Appium driver.
from support.locators import Element, Locator
from support.pages.base import BasePage


class HomePage(BasePage):
    PRODUCTS_LABEL = Element.label(
        name='Products',
        ios_query=(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="PRODUCTS"]'),
        android_query=(AppiumBy.ANDROID_UIAUTOMATOR, get_text('PRODUCTS')),
        web_query=(SeleniumBy.XPATH, '/html/body/div[2]/header')
    )

    USERNAME_LABEL = Element.label(
        name='Username',
        ios_query=(AppiumBy.NAME, 'Username'),
        android_query=(AppiumBy.ANDROID_UIAUTOMATOR, get_description('test-Username')),
        web_query=(SeleniumBy.XPATH, '/html/body/div[2]/header')
    )

    def __init__(self, context):
        super().__init__(context)

    @property
    def previous_screen(self):
        from pages import LoginPage
        return LoginPage(self.context)

    @property
    def trait(self) -> Element:
        return self.PRODUCTS_LABEL

    @property
    def path_switcher(self):
        pass