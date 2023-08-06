from functools import wraps
from typing import Callable, Dict, Any

SessionResult = Dict


# noinspection SpellCheckingInspection
# Add a decorator to the method to automatically open the session when you enter the method
def sqlsession(factory: Any) -> Callable:
    # Gets the session factory location
    @wraps(factory)
    def decorator(func):
        # Method to add a decorator
        @wraps(func)
        def wrapper(*args, **kwargs) -> SessionResult:
            session_result = {}

            # Encapsulate as a new method
            def handle():
                session_result["data"] = func(*args, **kwargs)

            # Perform the session
            session_result["exception"] = factory.transaction(handle)
            return session_result
        return wrapper
    return decorator
