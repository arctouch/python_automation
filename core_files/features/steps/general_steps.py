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
from __future__ import absolute_import

from behave import given, when, then

from support.locators import Element
from support.pages.page_factory import get_page_by_name


# Given steps
@given('the app displays the "{page_name}" screen')
def given_app_displays_page(context, page_name):
    page = get_page_by_name(context, page_name)
    if not page.is_current_page:
        page.navigate()

    assert page.is_current_page
    context.page = page


@given('the app displays the "{prompt}" prompt')
def given_app_displays_prompt(context, prompt):
    given_app_displays_page(context, prompt)


# When steps
@when('the user taps on the "{button_name}" button')
def when_user_taps_button(context, button_name):
    element = Element.button(button_name)
    context.page.tap_element(element)


@when('the user types "{value}" on the "{field_name}" field')
def when_enters_value(context, value, field_name):
    element = Element.input(field_name)
    context.page.send_value(element, value)


@when('the user taps on the item at position "{position}"')
def step_impl(context, position):
    context.page.tap_cell_at_position(position)


# Then steps
@then('the app should display the "{image}" logo')
def then_app_display_image(context, image):
    assert context.page.element_is_displayed(Element.image(image)), \
        "Image '{}' not displayed in '{}'".format(image, context.page.name)


@then('the app should display the "{label}" label')
def then_app_display_label(context, label):
    assert context.page.element_is_displayed(Element.label(label))


@then('the app should display the "{label}" text')
def then_app_display_text(context, label):
    then_app_display_label(context, label)


@then('the app should display the "{prompt_name}" prompt')
def then_app_display_prompt(context, prompt_name):
    assert context.page.element_is_displayed(Element.prompt(prompt_name))


@then('the app should display the "{image}" image')
def then_app_display_logo(context, image):
    then_app_display_image(context, image)


@then('the app should display the "{page_name}" screen')
def assert_the_app_displays_page(context, page_name):
    page = get_page_by_name(context, page_name)
    assert page.wait_to_be_current_page(), "Page '{}' was not displayed".format(page_name)
    context.page = page


@then('the app should display the "{field_name}" field')
def then_app_display_field(context, field_name):
    element = Element.input(field_name)
    context.page.element_is_displayed(element)


@then('the app should display the "{button_name}" button')
def then_app_display_button(context, button_name):
    element = Element.button(button_name)
    context.page.element_is_displayed(element)
