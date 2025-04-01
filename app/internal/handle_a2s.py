from functools import wraps
from fastapi import HTTPException
from socket import timeout, gaierror
from a2s import BrokenMessageError, BufferExhaustedError

def handle_a2s_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError:
            raise HTTPException(502, "Connection refused")
        except timeout:
            raise HTTPException(504, "Request timed out")
        except gaierror:
            raise HTTPException(400, "Invalid address")
        except BrokenMessageError(Exception):
            raise HTTPException(502, "Decoding error")
        except BufferExhaustedError(BrokenMessageError):
            raise HTTPException(502, "Response too short")
        except (OSError, Exception):
            raise HTTPException(500, "Internal server error")
    return wrapper
