from dataclasses import dataclass


@dataclass
class User(object):
    username: str
    password: str

