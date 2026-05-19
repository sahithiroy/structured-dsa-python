from enum import Enum


class SchemaNames(str, Enum):
    Default = "animal"


class CollectionNames(str, Enum):
    Cat = "cat"
    Dog = "dog"
