def get_text(string):
    """Will return the parameter used to search for the specified string"""
    return 'new UiSelector().text(\"{0}\")'.format(string)


def get_description(string):
    """Will return the parameter used to search for the specified content-desc"""
    return 'new UiSelector().description(\"{0}\")'.format(string)


def select_button_with_text(text):
    return 'new UiSelector().className("android.widget.Button").text("{}")'.format(text)


def select_edit_text(text):
    return 'new UiSelector().className("android.widget.EditText").text("{}")'.format(text)
