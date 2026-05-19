
from enum import Enum

class DogBreed(Enum):
    LABRADOR = "Labrador Retriever"
    GERMAN_SHEPHERD = "German Shepherd"
    GOLDEN_RETRIEVER = "Golden Retriever"
    FRENCH_BULLDOG = "French Bulldog"
    BEAGLE = "Beagle"

class GenderEnum(int,Enum):
    male =1
    female = 2
