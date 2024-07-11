import typing_extensions as typing


class Person(typing.TypedDict):
    "JSON schema for person information"

    clothes: str


class Vehicle(typing.TypedDict):
    "JSON schema for vehicle information"

    type: str
    color: str
    model: str


class Scene(typing.TypedDict):
    "JSON schema for a scene composed of persons and vehicles"

    persons: typing.List[Person]
    vehicles: typing.List[Vehicle]
