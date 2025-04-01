from fastapi import Depends, FastAPI

from .routers import server

app = FastAPI()

app.include_router(server.router)
