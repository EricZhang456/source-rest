from fastapi import FastAPI

from .routers import server

description = """
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
    title = "source-rest",
    description = description,
    summary = "A RESTful API wrapper for the Source engine A2S query protocol.",
    version = "1.0",
    license_info = {
        "name": "Apache 2.0",
        "identifier": "Apache-2.0",
    },
    openapi_tags=tags_metadata
)

app.include_router(server.router)
