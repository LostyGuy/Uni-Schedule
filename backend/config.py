import os

def get_environmental_variables(name: str) -> str:
    
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environmental value '{name}' is not set")
    
    return value