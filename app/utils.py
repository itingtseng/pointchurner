from .models.db import environment, SCHEMA

def add_prefix_for_prod(name):
    """
    Adds a schema prefix to table names in production.
    """
    if environment == "production":
        return f"{SCHEMA}.{name}"
    return name
