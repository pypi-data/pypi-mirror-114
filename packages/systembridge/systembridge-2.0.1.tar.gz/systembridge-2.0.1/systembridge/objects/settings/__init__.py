"""
Class object for Settings
Documentation: https://system-bridge.timmo.dev
"""
from __future__ import annotations
from ..base import BridgeBase


class Settings(BridgeBase):
    @property
    def section(self) -> str:
        return self.attributes.get("section", None)

    @property
    def key(self) -> str:
        return self.attributes.get("key", None)

    @property
    def name(self) -> str:
        return self.attributes.get("name", None)

    @property
    def description(self) -> str:
        return self.attributes.get("description", None)

    @property
    def defaultValue(self) -> str:
        return self.attributes.get("defaultValue", None)

    @property
    def value(self) -> str | float | int | bool:
        return self.attributes.get("value", None)

    @property
    def icon(self) -> str:
        return self.attributes.get("icon", None)

    @property
    def requiresServerRestart(self) -> bool:
        return self.attributes.get("requiresServerRestart", False)
