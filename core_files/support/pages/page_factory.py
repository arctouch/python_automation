import pages

PAGES_BY_NAME = dict([(name, cls) for name, cls in pages.__dict__.items() if isinstance(cls, type)])


def get_page_by_name(context, page_name):
    no_spaces_name = page_name.replace(" ", "")
    page_type_name = "{name}Page".format(name=no_spaces_name)

    return PAGES_BY_NAME[page_type_name](context)
