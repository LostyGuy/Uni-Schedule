import os

from hashlib import sha256 as algorithm
from backend.config import get_environmental_variables

HASH_SALT = get_environmental_variables("HASH_SALT")

def hash_string(input , hash_salt = HASH_SALT) -> str:
    return algorithm((input + hash_salt).encode()).hexdigest()