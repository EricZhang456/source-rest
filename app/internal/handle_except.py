from fastapi import status
from fastapi.responses import JSONResponse


def handle_connection_refused(*_):
    return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY,
                        content={"error": "Connection refused"})


def handle_request_timed_out(*_):
    return JSONResponse(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                        content={"error": "Request timed out"})


def handle_invalid_addr(*_):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"error": "Invalid address"})


def handle_decode_error(*_):
    return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY,
                        content={"error": "Decoding error"})


def handle_response_too_short(*_):
    return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY,
                        content={"error": "Response too short"})
