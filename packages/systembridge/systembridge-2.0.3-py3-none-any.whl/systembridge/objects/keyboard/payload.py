"""
Class object for KeyboardPayload
Documentation: https://system-bridge.timmo.dev
"""
from typing import List, Optional
from ..base import BridgeBase


class KeyboardPayload(BridgeBase):
    @property
    def key(self) -> Optional[str]:
        return self.attributes.get("key", "")

    @property
    def modifiers(self) -> Optional[List[str]]:
        return self.attributes.get("modifiers", [])

    @property
    def text(self) -> Optional[str]:
        return self.attributes.get("text", "")
