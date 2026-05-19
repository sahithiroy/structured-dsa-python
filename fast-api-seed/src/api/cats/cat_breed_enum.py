from enum import Enum


# Enum class to represent cat breeds
class CatBreed(str, Enum):
    siamese = "Siamese"
    persian = "Persian"
    maine_coon = "Maine Coon"
    sphynx = "Sphynx"
    null = ""
