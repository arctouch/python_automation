from dataclasses import dataclass, field
from enum import Enum, auto


class Locator:

    def __init__(self, ios=None, android=None, web=None) -> None:
        self._ios = ios
        self._android = android
        self._web = web

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def ios(self):
        return self._ios

    @property
    def android(self):
        return self._android

    @property
    def web(self):
        return self._web

    def query(self, platform):
        return self[platform]

    def __repr__(self) -> str:
        return "Locator <ios = '{}', android = '{}', web = '{}'>".format(self.ios, self.android, self.web)


@dataclass(frozen=True)
class Element:
    class Kind(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name.lower()

        VIEW = auto()
        LABEL = auto()
        BUTTON = auto()
        SECTION = auto()
        INPUT = auto()
        PROMPT = auto()
        CELL = auto()
        IMAGE = auto()
        TABLE = auto()
        TAB = auto()

        def __repr__(self):
            return "'{}'".format(self.value)

    kind: Kind
    name: str = field(default=None)
    position: int = field(default=None)
    locator: Locator = field(default=None, compare=None, hash=None)

    @property
    def identity(self):
        position = ", position='{}'".format(self.position) if self.position is not None else ""
        return "Element <kind='{}', name='{}'{}>".format(self.kind, self.name, position)

    @staticmethod
    def view(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.VIEW, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def label(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.LABEL, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def button(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.BUTTON, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def section(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.SECTION, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def input(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.INPUT, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def prompt(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.PROMPT, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def table(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.PROMPT, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def tab(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.TAB, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def image(name, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.IMAGE, name, locator=Locator(ios=ios_query, android=android_query, web=web_query))

    @staticmethod
    def cell(position, ios_query=None, android_query=None, web_query=None):
        return Element(Element.Kind.CELL, position=position, locator=Locator(ios=ios_query, android=android_query, web=web_query))

