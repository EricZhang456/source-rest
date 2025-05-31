from typing import Annotated, NotRequired, TypedDict

import a2s
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel


class InfoResponse(TypedDict):
    protocol: int
    version: str
    name: str
    map: str
    folder: str
    game: str
    player_count: int
    max_players: int
    bot_count: int
    server_type: str
    platform: str
    password: bool
    vac: bool
    ping: float
    tags: NotRequired[list[str]]
    appid: NotRequired[int]
    edf: NotRequired[int]
    port: NotRequired[int]
    steam_id: NotRequired[int]
    stv_port: NotRequired[int]
    stv_name: NotRequired[str]
    gameid: NotRequired[int]
    address: NotRequired[str]
    is_mod: NotRequired[bool]
    mod_website: NotRequired[str]
    mod_download: NotRequired[str]
    mod_version: NotRequired[int]
    mod_size: NotRequired[int]
    multiplayer_only: NotRequired[bool]
    uses_custom_dll: NotRequired[bool]


class PlayerListItem(BaseModel):
    index: int
    name: str
    score: int
    time: float


router = APIRouter()


@router.get("/server/rules/{server_ip}/", name="Fetch Server Rules", tags=["server"])
async def get_server_rules(server_ip: Annotated[str,
                                                Path(title="Server IP",
                                                     description="IP or hostname of the server.")],
                           server_port: Annotated[int,
                                                  Query(gt=0, le=65535,
                                                        title="Server Port",
                                                        description="Port of the server.")] = 27015) -> dict:
    """
    Fetch the rules of a server. This would be every cvar with the
    [FCVAR_NOTIFY](https://developer.valvesoftware.com/wiki/FCVAR_NOTIFY) flag.
    """
    server_address = (server_ip, server_port)
    return await a2s.arules(server_address)


@router.get("/server/info/{server_ip}/", name="Fetch Server Info", tags=["server"],
            response_model=InfoResponse)
async def get_server_info(server_ip: Annotated[str,
                                               Path(title="Server IP",
                                                    description="IP or hostname of the server.")],
                          server_port: Annotated[int,
                                                 Query(gt=0, le=65535, title="Server Port",
                                                       description="Port of the server.")] = 27015) -> dict:
    """Fetch information about a server."""
    server_address = (server_ip, server_port)
    server_info_raw = await a2s.ainfo(server_address)
    server_info = {
        "protocol": server_info_raw.protocol,
        "version": server_info_raw.version,
        "name": server_info_raw.server_name,
        "map": server_info_raw.map_name,
        "folder": server_info_raw.folder,
        "game": server_info_raw.game,
        "player_count": server_info_raw.player_count,
        "max_players": server_info_raw.max_players,
        "bot_count": server_info_raw.bot_count,
        "server_type": server_info_raw.server_type,
        "platform": server_info_raw.platform,
        "password": server_info_raw.password_protected,
        "vac": server_info_raw.vac_enabled,
        "ping": server_info_raw.ping,
    }

    if server_info_raw.keywords:
        server_info["tags"] = tuple(filter(None, server_info_raw.keywords.split(",")))

    if type(server_info_raw).__name__ == "SourceInfo":
        additional_attrs = {"app_id": "appid", "edf": "edf"}
        optional_attrs = ("port", "steam_id", "stv_port", "stv_name", "game_id")
        for key, value in additional_attrs.items():
            server_info.update({value: getattr(server_info_raw, key)})
        for item in optional_attrs:
            if getattr(server_info_raw, item) is not None:
                server_info.update({item: getattr(server_info_raw, item)})

    # goldsrc responds to queries the same way as source does now but this
    # check is kept for good measures
    if type(server_info_raw).__name__ == "GoldSrcInfo":
        additional_attrs = ("address", "is_mod",
                            "mod_website", "mod_download",
                            "mod_version", "mod_size",
                            "multiplayer_only", "uses_custom_dll")
        for item in additional_attrs:
            if getattr(server_info_raw, item) is not None:
                server_info.update({item: getattr(server_info_raw, item)})

    return server_info


@router.get("/server/players/{server_ip}/", name="Fetch Player List", tags=["server"],
            response_model=list[PlayerListItem])
async def get_server_players(server_ip: Annotated[str,
                                                  Path(title="Server IP",
                                                       description="IP or hostname of the server.")],
                             server_port: Annotated[int,
                                                    Query(gt=0, le=65535, title="Server Port",
                                                          description="Port of the server.")] = 27015) -> list[dict]:
    """Fetch a list of players on a server."""
    server_address = (server_ip, server_port)
    server_players_raw = await a2s.aplayers(server_address)
    server_players = []
    for item in server_players_raw:
        player = {"index": item.index, "name": item.name,
                  "score": item.score, "time": item.duration}
        server_players.append(player)
    return server_players
