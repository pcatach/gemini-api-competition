import typing_extensions as typing


class Person(typing.TypedDict):
    "JSON schema for person information"

    clothes: str
    gender: typing.Literal["male", "female", "unsure"]


class Vehicle(typing.TypedDict):
    "JSON schema for vehicle information"

    type: str
    color: str


class Environment(typing.TypedDict):
    "JSON schema for environment information"

    weather: str
    summary: str


class Scene(typing.TypedDict):
    "JSON schema for a scene composed of persons and vehicles"

    environment: Environment
    persons: typing.List[Person]
    vehicles: typing.List[Vehicle]
