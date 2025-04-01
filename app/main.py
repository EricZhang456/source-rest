from fastapi import FastAPI

from .routers import server

description = """
Functions:
* Get Server Info
* Get Server Rules
* Get Players in a Server
"""

tags_metadata = [
    {
        "name": "rules",
        "description": "Fetch the rules of a server. This would be every cvar with the [FCVAR_NOTIFY](https://developer.valvesoftware.com/wiki/FCVAR_NOTIFY) flag.",
    },
    {
        "name": "info",
        "description": "Fetch information about a server."
    },
    {
        "name": "players",
        "description": "Fetch a list of players on a server."
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
