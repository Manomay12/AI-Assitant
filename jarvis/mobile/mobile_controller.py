# ==================================================
# JARVIS AI — Cross-Platform Mobile Controller
# ==================================================

import logging
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger("jarvis.mobile")


class MobileDevice(BaseModel):
    device_id: str
    device_name: str
    platform: str  # "android", "ios"
    paired_at: str
    is_active: bool = True
    capabilities: List[str] = []


class MobileController:
    """
    Manages authenticated mobile companion devices (Android/iOS).
    Handles device pairing, remote notifications, and permission authorization bridges.
    """

    def __init__(self):
        self._paired_devices: Dict[str, MobileDevice] = {}

    def pair_device(self, device_id: str, device_name: str, platform: str) -> MobileDevice:
        """Register and authorize a new mobile device."""
        device = MobileDevice(
            device_id=device_id,
            device_name=device_name,
            platform=platform,
            paired_at=datetime.now().isoformat(),
            capabilities=["notifications", "remote_voice", "status_monitor"],
        )
        self._paired_devices[device_id] = device
        logger.info(f"Paired mobile device: {device_name} ({platform})")
        return device

    def list_devices(self) -> List[MobileDevice]:
        return list(self._paired_devices.values())

    def unpair_device(self, device_id: str) -> bool:
        return self._paired_devices.pop(device_id, None) is not None


mobile_controller = MobileController()
