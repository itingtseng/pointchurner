from app.models.db import SCHEMA, environment

def add_prefix_for_prod(name):
    """
    Adds a schema prefix for production environments.
    """
    if environment == "production":
        return f"{SCHEMA}.{name}"
    return name
