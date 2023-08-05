"""Bridge: Init"""
from __future__ import annotations
from aiohttp import ClientResponse
from typing import Any, List

from .client import BridgeClient
from .client_websocket import BridgeClientWebSocket
from .objects.audio import Audio
from .objects.audio.put import AudioPutPayload, AudioPutResponse
from .objects.base import BridgeBase
from .objects.battery import Battery
from .objects.bluetooth import Bluetooth
from .objects.command.payload import CommandPayload
from .objects.command.response import CommandResponse
from .objects.cpu import Cpu
from .objects.display import Display
from .objects.display.put import DisplayPutPayload
from .objects.events import Event, EventBase
from .objects.filesystem import Filesystem
from .objects.graphics import Graphics
from .objects.information import Information
from .objects.keyboard.payload import KeyboardPayload
from .objects.keyboard.response import KeyboardResponse
from .objects.memory import Memory
from .objects.network import Network
from .objects.open.payload import OpenPayload
from .objects.os import Os
from .objects.processes import ProcessList, Processes
from .objects.settings import Settings
from .objects.settings.put import SettingsPutPayload
from .objects.system import System

BASE_HEADERS = {"Accept": "application/json"}


class Bridge(BridgeBase):
    """Main class for Bridge."""

    def __init__(self, client: BridgeClient, base_url: str, api_key: str) -> None:
        """Initialize the class."""
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._audio: Audio = {}
        self._battery: Battery = {}
        self._bluetooth: Bluetooth = {}
        self._cpu: Cpu = {}
        self._display: Display = {}
        self._filesystem: Filesystem = {}
        self._graphics: Graphics = {}
        self._information: Information = {}
        self._memory: Memory = {}
        self._network: Network = {}
        self._os: Os = {}
        self._processes: Processes = {}
        self._settings: List[Settings] = []
        self._system: System = {}
        self._websocket_client: BridgeClientWebSocket = None

    @property
    def audio(self) -> Audio:
        return self._audio

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def bluetooth(self) -> Bluetooth:
        return self._bluetooth

    @property
    def cpu(self) -> Cpu:
        return self._cpu

    @property
    def display(self) -> Display:
        return self._display

    @property
    def filesystem(self) -> Filesystem:
        return self._filesystem

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def information(self) -> Information:
        return self._information

    @property
    def memory(self) -> Memory:
        return self._memory

    @property
    def network(self) -> Network:
        return self._network

    @property
    def os(self) -> Os:
        return self._os

    @property
    def processes(self) -> Processes:
        return self._processes

    @property
    def settings(self) -> List[Settings]:
        return self._settings

    @property
    def system(self) -> System:
        return self._system

    async def async_post(self, path: str, payload: Any | None) -> Any:
        """Generic Delete"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_get(self, path: str) -> Any:
        """Generic get"""
        response: ClientResponse = await self._client.get(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_post(self, path: str, payload: Any) -> Any:
        """Generic post"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_put(self, path: str, payload: Any) -> Any:
        """Generic put"""
        response: ClientResponse = await self._client.put(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        if "application/json" in response.headers.get("Content-Type", ""):
            return await response.json()
        return await response.text()

    async def async_get_audio(self) -> Audio:
        """Get audio information"""
        self._audio = Audio(await self.async_get("/audio"))
        return self._audio

    async def async_update_audio(
        self, id: str, payload: AudioPutPayload
    ) -> AudioPutResponse:
        """Update audio"""
        return AudioPutResponse(await self.async_put(f"/audio/{id}", payload))

    async def async_get_battery(self) -> Battery:
        """Get battery information"""
        self._battery = Battery(await self.async_get("/battery"))
        return self._battery

    async def async_get_bluetooth(self) -> Bluetooth:
        """Get bluetooth information"""
        self._bluetooth = Bluetooth(await self.async_get("/bluetooth"))
        return self._bluetooth

    async def async_send_command(self, payload: CommandPayload) -> CommandResponse:
        """Send command"""
        return CommandResponse(await self.async_post("/command", payload))

    async def async_get_cpu(self) -> Cpu:
        """Get cpu information"""
        self._cpu = Cpu(await self.async_get("/cpu"))
        return self._cpu

    async def async_get_display(self) -> Cpu:
        """Get display information"""
        self._display = Display(await self.async_get("/display"))
        return self._display

    async def async_update_display(
        self, id: str, payload: DisplayPutPayload
    ) -> Display:
        """Update display"""
        return AudioPutResponse(await self.async_put(f"/display/{id}", payload))

    async def async_get_filesystem(self) -> Filesystem:
        """Get filesystem information"""
        self._filesystem = Filesystem(await self.async_get("/filesystem"))
        return self._filesystem

    async def async_get_graphics(self) -> Graphics:
        """Get graphics information"""
        self._graphics = Graphics(await self.async_get("/graphics"))
        return self._graphics

    async def async_get_information(self) -> Information:
        """Get information"""
        self._information = Information(await self.async_get("/information"))
        return self._information

    async def async_get_memory(self) -> Memory:
        """Get memory information"""
        self._memory = Memory(await self.async_get("/memory"))
        return self._memory

    async def async_get_network(self) -> Network:
        """Get network information"""
        self._network = Network(await self.async_get("/network"))
        return self._network

    async def async_open(self, payload: OpenPayload) -> OpenPayload:
        """Send command"""
        return OpenPayload(await self.async_post("/open", payload))

    async def async_get_os(self) -> Os:
        """Get os information"""
        self._os = Os(await self.async_get("/os"))
        return self._os

    async def async_get_processes(self) -> Processes:
        """Get processes information"""
        self._processes = Processes(await self.async_get("/processes"))
        return self._processes

    async def async_get_process(self, name: str) -> Processes:
        """Get process from name"""
        self._processes = ProcessList(await self.async_get(f"/processes/{name}"))
        return self._processes

    async def async_get_settings(self) -> List[Settings]:
        """Get settings"""
        settings = await self.async_get("/settings")
        self._settings = [Settings(setting) for setting in settings]
        return self._settings

    async def async_get_setting(self, section: str, key: str) -> Settings:
        """Get setting"""
        return Settings(await self.async_get(f"/settings/{section}/{key}"))

    async def async_update_setting(
        self, section: str, key: str, payload: SettingsPutPayload
    ) -> Settings:
        """Update setting"""
        return Settings(await self.async_put(f"/settings/{section}/{key}", payload))

    async def async_get_system(self) -> System:
        """Get system information"""
        self._system = System(await self.async_get("/system"))
        return self._system

    async def async_send_keypress(self, payload: KeyboardPayload) -> KeyboardResponse:
        """Send keypress"""
        return KeyboardResponse(await self.async_post("/keyboard", payload))

    async def async_connect_websocket(self, host: str, port: int) -> None:
        self._websocket_client: BridgeClientWebSocket = BridgeClientWebSocket(
            self._api_key
        )
        await self._websocket_client.connect(f"ws://{host}:{port}")
        await self._websocket_client.register_listener()

    async def async_send_event(self, event: str, data: Event) -> None:
        await self._websocket_client.send_event(event, data)

    async def listen_for_events(self, callback: function) -> None:
        async def handle_message(message: EventBase) -> None:
            if "data" in message and type(message["data"]) is dict:
                event = Event(message["data"])
                if "data-" in event.name:
                    name = event.name.replace("data-", "")
                    if name == "audio":
                        self._audio = Audio(event.data)
                    elif name == "battery":
                        self._battery = Battery(event.data)
                    elif name == "bluetooth":
                        self._bluetooth = Bluetooth(event.data)
                    elif name == "cpu":
                        self._cpu = Cpu(event.data)
                    elif name == "display":
                        self._display = Display(event.data)
                    elif name == "filesystem":
                        self._filesystem = Filesystem(event.data)
                    elif name == "graphics":
                        self._graphics = Graphics(event.data)
                    elif name == "information":
                        self._information = Information(event.data)
                    elif name == "memory":
                        self._memory = Memory(event.data)
                    elif name == "network":
                        self._network = Network(event.data)
                    elif name == "os":
                        self._os = Os(event.data)
                    elif name == "processes":
                        self._processes = Processes(event.data)
                    elif name == "settings":
                        self._settings = [Settings(setting) for setting in event.data]
                    elif name == "system":
                        self._system = System(event.data)
                await callback(event)

        await self._websocket_client.listen_for_messages(handle_message)
