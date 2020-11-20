# Copyright 2020 ArcTouch LLC (authored by Thiago Werner at ArcTouch)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
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