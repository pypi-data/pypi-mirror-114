"""Bridge: ClientWebSocket"""
from __future__ import annotations
import asyncio
import json
from systembridge.exceptions import BridgeException
import websockets

from typing import Any
from websockets import ClientConnection, ConnectionClosed

from ..objects.base import BridgeBase


class BridgeClientWebSocket(BridgeBase):
    """Client to handle websocket communication."""

    def __init__(self, api_key: str) -> None:
        self._api_key: str = api_key
        self._websocket: ClientConnection = None

    async def connect(self, uri: str) -> None:
        self._websocket: ClientConnection = await websockets.connect(uri)

    async def authenticate(self) -> None:
        await self._websocket.send(
            json.dumps(
                {
                    "event": "register-listener",
                    "data": {"api-key": self._api_key},
                }
            )
        )

    async def send_event(self, event: str, data: Any | None) -> None:
        await self._websocket.send(
            json.dumps(
                {
                    "event": "events",
                    "data": {
                        "api-key": self._api_key,
                        "data": {
                            "name": event,
                            "data": data,
                        },
                    },
                }
            )
        )

    async def listen_for_messages(self, callback: function) -> None:
        while True:
            await asyncio.sleep(0)
            try:
                message = await self._websocket.recv()
                await callback(json.loads(message))
            except ConnectionClosed as e:
                raise BridgeException from e
