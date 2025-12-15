#!/usr/bin/env python3
"""
WDW Monorail Fleet Management
All 14 monorails: 12 active + 2 retired (post-2009 accident)
"""

import logging
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

class MonorailLine(Enum):
    RESORT = "resort"
    EXPRESS = "express"
    EXPRESS_EPCOT = "express_epcot"

@dataclass
class Monorail:
    name: str
    color: str
    hex_color: str
    train_number: int
    operational: bool
    line: Optional[MonorailLine] = None
    status: str = "idle"
    position: float = 0.0
    speed: float = 0.0
    
    def get_display_name(self) -> str:
        status_str = "🟢 ACTIVE" if self.operational else "🔴 RETIRED"
        return f"{self.color} Train ({self.name}) - {status_str}"

class MonorailFleet:
    """Manages all 14 WDW monorails"""
    
    def __init__(self):
        self.monorails: dict = {}
        self._initialize_fleet()
    
    def _initialize_fleet(self):
        """Initialize all 12 active + 2 retired monorails"""
        
        # ACTIVE MONORAILS (12)
        active_trains = [
            Monorail("Red", "Red", "#FF0000", 1, True),
            Monorail("Orange", "Orange", "#FFA500", 2, True),
            Monorail("Yellow", "Yellow", "#FFFF00", 3, True),
            Monorail("Green", "Green", "#00AA00", 4, True),
            Monorail("Blue", "Blue", "#0000FF", 5, True),
            Monorail("Purple", "Purple", "#800080", 6, True),
            Monorail("Pink", "Pink", "#FF69B4", 7, True),
            Monorail("Coral", "Coral", "#FF7F50", 8, True),
            Monorail("Teal", "Teal", "#008080", 9, True),
            Monorail("Silver", "Silver", "#C0C0C0", 10, True),
            Monorail("Gold", "Gold", "#FFD700", 11, True),
            Monorail("Lime", "Lime", "#00FF00", 12, True),
        ]
        
        # RETIRED MONORAILS (2) - Post-2009 Accident
        retired_trains = [
            Monorail("White", "White (Retired)", "#FFFFFF", 13, False),  # Retired after 2009 accident
            Monorail("Black", "Black (Retired)", "#000000", 14, False),  # Retired after 2009 accident
        ]
        
        # Register all trains
        for train in active_trains + retired_trains:
            self.monorails[f"monorail-{train.train_number}"] = train
    
    def get_fleet(self) -> dict:
        """Get all monorails"""
        return self.monorails
    
    def get_active_fleet(self) -> dict:
        """Get only active monorails (12)"""
        return {k: v for k, v in self.monorails.items() if v.operational}
    
    def get_retired_fleet(self) -> dict:
        """Get retired monorails (2)"""
        return {k: v for k, v in self.monorails.items() if not v.operational}
    
    def get_monorail(self, monorail_id: str) -> Optional[Monorail]:
        """Get specific monorail by ID"""
        return self.monorails.get(monorail_id)
    
    def get_monorails_by_line(self, line: MonorailLine) -> dict:
        """Get all monorails assigned to a specific line"""
        return {k: v for k, v in self.monorails.items() 
                if v.operational and v.line == line}
    
    def assign_to_line(self, monorail_id: str, line: MonorailLine) -> bool:
        """Assign monorail to a line"""
        train = self.get_monorail(monorail_id)
        if train and train.operational:
            train.line = line
            logging.info(f"[{train.color}] Assigned to {line.value} line")
            return True
        elif train and not train.operational:
            logging.error(f"[{train.color}] Cannot assign retired train to line")
            return False
        return False
    
    def get_fleet_summary(self) -> dict:
        """Get fleet summary statistics"""
        active = self.get_active_fleet()
        retired = self.get_retired_fleet()
        
        lines = {
            "resort": len(self.get_monorails_by_line(MonorailLine.RESORT)),
            "express": len(self.get_monorails_by_line(MonorailLine.EXPRESS)),
            "express_epcot": len(self.get_monorails_by_line(MonorailLine.EXPRESS_EPCOT)),
        }
        
        return {
            "total_fleet": len(self.monorails),
            "active_count": len(active),
            "retired_count": len(retired),
            "retired_year": 2009,
            "retired_reason": "Monorail accident",
            "monorails_by_line": lines,
            "active_monorails": [f"{v.color} (Train {v.train_number})" for v in active.values()],
            "retired_monorails": [f"{v.color} (Train {v.train_number})" for v in retired.values()],
        }
    
    def display_fleet(self):
        """Display all monorails"""
        logging.info("=" * 70)
        logging.info("WDW MONORAIL FLEET - ALL 14 TRAINS")
        logging.info("=" * 70)
        
        logging.info("\n🟢 ACTIVE MONORAILS (12):")
        logging.info("-" * 70)
        for train_id, train in self.get_active_fleet().items():
            line_str = f"Line: {train.line.value}" if train.line else "Unassigned"
            logging.info(f"  {train.get_display_name()} | {line_str}")
        
        logging.info("\n🔴 RETIRED MONORAILS (2) - Post-2009 Accident:")
        logging.info("-" * 70)
        for train_id, train in self.get_retired_fleet().items():
            logging.info(f"  {train.get_display_name()} | Train #{train.train_number}")
        
        logging.info("\n" + "=" * 70)
        summary = self.get_fleet_summary()
        logging.info(f"Total Fleet: {summary['total_fleet']} trains")
        logging.info(f"  • Active: {summary['active_count']}")
        logging.info(f"  • Retired: {summary['retired_count']} (since {summary['retired_year']})")
        logging.info("=" * 70 + "\n")

async def demo_fleet():
    """Demo fleet management"""
    fleet = MonorailFleet()
    fleet.display_fleet()
    
    # Assign some to lines
    fleet.assign_to_line("monorail-1", MonorailLine.RESORT)
    fleet.assign_to_line("monorail-2", MonorailLine.EXPRESS)
    fleet.assign_to_line("monorail-3", MonorailLine.EXPRESS_EPCOT)
    
    logging.info("\n📊 Fleet Summary:")
    summary = fleet.get_fleet_summary()
    for key, value in summary.items():
        logging.info(f"  {key}: {value}")
    
    logging.info("\n✅ Fleet management demo complete!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_fleet())

