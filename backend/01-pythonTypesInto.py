'''
This module contains the FastAPI application and its routes. It defines the endpoints for the API and handles incoming requests. 
The application is built using the FastAPI framework, which provides a simple and efficient way to create web APIs with Python.

'''
from fastapi import FastAPI

def get_full_name(first_name:str,last_name:str)->str:
    return first_name+""+last_name
'''
from typing import Any
def sahithi(first_name:str,last_name:str)->Any:
    return first_name+""+last_name
'''