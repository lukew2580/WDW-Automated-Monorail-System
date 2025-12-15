#!/usr/bin/env python3
"""
WDW Automated Monorail System - Bluetooth Controller
Controls Disney monorail trains with line awareness
"""

import asyncio
import logging
from enum import Enum
from dataclasses import dataclass
from line_management import MonorailLineTracker, MonorailLine

class MonorailController:
    """Controls a single monorail train with line awareness"""
    
    def __init__(self, monorail_id: str, mac_address: str):
        self.monorail_id = monorail_id
        self.mac_address = mac_address
        self.line_tracker = MonorailLineTracker(monorail_id)
        self.is_running = False
        self.current_speed = 0.0
    
    async def set_line(self, line: MonorailLine) -> bool:
        """Assign this monorail to a specific WDW line"""
        return await self.line_tracker.set_line(line)
    
    async def get_status(self) -> dict:
        """Get detailed status including line information"""
        base_status = {
            "monorail_id": self.monorail_id,
            "is_running": self.is_running,
            "current_speed": self.current_speed,
        }
        line_status = self.line_tracker.get_line_status()
        return {**base_status, **line_status}

if __name__ == "__main__":
    asyncio.run(main())


