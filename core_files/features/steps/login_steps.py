from behave import when, use_step_matcher

from pages import LoginPage

use_step_matcher("re")


@when("the user types his credentials")
def type_credentials(context):
    page = LoginPage(context)
    assert page.is_current_page, "{} is not current page".format(page)
    page.type_credentials(context.user)
