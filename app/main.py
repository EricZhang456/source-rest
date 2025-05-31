from asyncio.exceptions import TimeoutError
from socket import gaierror

from fastapi import FastAPI
from a2s import BrokenMessageError, BufferExhaustedError

from .routers import server
from .internal.handle_except import (handle_connection_refused, handle_decode_error,
                                     handle_invalid_addr, handle_request_timed_out,
                                     handle_response_too_short)

DESCRIPTION = """
Functions:
* Fetch Server Info
* Fetch Server Rules
* Fetch Players in a Server
"""

tags_metadata = [
    {
        "name": "server",
        "description": "Get information about a server.",
    }
]

app = FastAPI(
    title="source-rest",
    description=DESCRIPTION,
    summary="A RESTful API wrapper for the Source engine A2S query protocol.",
    version="1.0",
    license_info={
        "name": "Apache 2.0",
        "identifier": "Apache-2.0",
    },
    openapi_tags=tags_metadata
)

app.include_router(server.router)

app.add_exception_handler(ConnectionRefusedError, handle_connection_refused)
app.add_exception_handler(TimeoutError, handle_request_timed_out)
app.add_exception_handler(gaierror, handle_invalid_addr)
app.add_exception_handler(BrokenMessageError, handle_decode_error)
app.add_exception_handler(BufferExhaustedError, handle_response_too_short)
