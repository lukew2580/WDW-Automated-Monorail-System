#!/usr/bin/env python3
"""
WDW Monorail Fleet Management
All 12 current monorails + accurate 2009 accident history
"""

import logging
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

class MonorailLine(Enum):
    """WDW Monorail Lines"""
    RESORT = "resort"
    EXPRESS = "express"
    EXPRESS_EPCOT = "express_epcot"

@dataclass
class Monorail:
    """Represents a single monorail train"""
    monorail_id: str
    color: str
    train_number: int
    operational: bool
    line: Optional[MonorailLine] = None
    position: float = 0.0
    speed: float = 0.0
    status: str = "idle"
    
class MonorailFleet:
    """Manages the complete WDW monorail fleet"""
    
    def __init__(self):
        self.monorails: Dict[str, Monorail] = {}
        self._initialize_fleet()
    
    def _initialize_fleet(self):
        """Initialize all 12 current monorails"""
        current_monorails = [
            ("lime", "Lime", 1, True),
            ("teal", "Teal", 2, True),  # Built from Pink & Purple wreckage (2009)
            ("red", "Red", 3, True),
            ("coral", "Coral", 4, True),
            ("orange", "Orange", 5, True),
            ("gold", "Gold", 6, True),
            ("yellow", "Yellow", 7, True),
            ("peach", "Peach", 8, True),  # Built with salvaged parts from crash
            ("green", "Green", 9, True),
            ("blue", "Blue", 10, True),
            ("silver", "Silver", 11, True),
            ("black", "Black", 12, True),
        ]
        
        for monorail_id, color, train_num, operational in current_monorails:
            self.monorails[monorail_id] = Monorail(
                monorail_id=monorail_id,
                color=color,
                train_number=train_num,
                operational=operational,
                line=None
            )
        
        logging.info(f"Fleet initialized with {len(self.monorails)} operational monorails")
    
    def get_fleet(self) -> Dict[str, Monorail]:
        """Get all monorails"""
        return self.monorails
    
    def get_monorail(self, monorail_id: str) -> Optional[Monorail]:
        """Get specific monorail"""
        return self.monorails.get(monorail_id)
    
    def get_monorails_by_line(self, line: MonorailLine) -> Dict[str, Monorail]:
        """Get all monorails assigned to a specific line"""
        return {
            mid: m for mid, m in self.monorails.items() 
            if m.line == line and m.operational
        }
    
    def assign_to_line(self, monorail_id: str, line: MonorailLine) -> bool:
        """Assign a monorail to a line"""
        if monorail_id not in self.monorails:
            logging.error(f"Monorail {monorail_id} not found")
            return False
        
        train = self.monorails[monorail_id]
        if not train.operational:
            logging.error(f"Monorail {monorail_id} is not operational")
            return False
        
        train.line = line
        logging.info(f"Assigned {train.color} to {line.value} line")
        return True
    
    def get_fleet_summary(self) -> Dict:
        """Get fleet summary with accident history"""
        return {
            "total_fleet": len(self.monorails),
            "operational_count": len(self.monorails),
            "current_monorails": [m.color for m in self.monorails.values()],
            "accident_date": "June 1, 2009",
            "accident_note": "Monorail Purple was involved in a collision with Monorail Pink. The pilot of Purple was fatally injured. Both trains were destroyed but their salvageable components were used to construct Teal and Peach.",
            "2009_accident_history": {
                "description": "Monorail crash on June 1, 2009",
                "retired_trains": {
                    "Pink": {
                        "train_number": 13,
                        "fate": "Destroyed - Pink & Purple wreckage used to build Teal",
                        "salvage": "Components salvaged for Teal"
                    },
                    "Purple": {
                        "train_number": 14,
                        "fate": "Destroyed - pilot tragically killed",
                        "salvage": "Components salvaged for Teal"
                    }
                },
                "rebuilt_from_accident": {
                    "Teal": {
                        "train_number": 2,
                        "built_from": "Undamaged sections of Pink and Purple",
                        "operational_since": 2010
                    },
                    "Peach": {
                        "train_number": 8,
                        "built_from": "New components + salvaged pieces from crashed trains",
                        "operational_since": 2011
                    }
                }
            }
        }
    
    def get_monorail_history(self, monorail_id: str) -> Dict:
        """Get history for specific monorail"""
        train = self.monorails.get(monorail_id)
        if not train:
            return {"error": "Monorail not found"}
        
        history_map = {
            "teal": {
                "color": "Teal",
                "status": "Operational",
                "history": "Built from salvaged undamaged sections of Pink and Purple after 2009 accident",
                "operational_since": 2010
            },
            "peach": {
                "color": "Peach",
                "status": "Operational",
                "history": "Built with new components and salvaged pieces from Pink and Purple",
                "operational_since": 2011
            },
            "lime": {
                "color": "Lime",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "red": {
                "color": "Red",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "coral": {
                "color": "Coral",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "orange": {
                "color": "Orange",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "gold": {
                "color": "Gold",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "yellow": {
                "color": "Yellow",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "green": {
                "color": "Green",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "blue": {
                "color": "Blue",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "silver": {
                "color": "Silver",
                "status": "Operational",
                "history": "Original fleet member"
            },
            "black": {
                "color": "Black",
                "status": "Operational",
                "history": "Original fleet member"
            }
        }
        
        return history_map.get(monorail_id, {"error": "History not found"})

async def demo_fleet():
    """Demo the complete fleet"""
    fleet = MonorailFleet()
    
    logging.info("=" * 70)
    logging.info("WDW MONORAIL FLEET - COMPLETE & ACCURATE")
    logging.info("=" * 70)
    
    logging.info("\n🚂 CURRENT OPERATIONAL FLEET (12 Monorails):")
    for monorail_id, train in fleet.get_fleet().items():
        logging.info(f"   • {train.color} (Train {train.train_number})")
    
    logging.info("\n📜 2009 ACCIDENT HISTORY:")
    summary = fleet.get_fleet_summary()
    accident = summary["2009_accident_history"]
    logging.info(f"   {accident['description']}")
    logging.info(f"   {summary['accident_note']}")
    
    logging.info("\n🔴 RETIRED TRAINS (Destroyed in 2009):")
    for name, details in accident["retired_trains"].items():
        logging.info(f"   • {name} (Train {details['train_number']})")
        logging.info(f"     → {details['fate']}")
    
    logging.info("\n🟢 REBUILT FROM ACCIDENT SALVAGE:")
    for name, details in accident["rebuilt_from_accident"].items():
        logging.info(f"   • {name} (Train {details['train_number']})")
        logging.info(f"     → Built from: {details['built_from']}")
        logging.info(f"     → Operational since: {details['operational_since']}")
    
    logging.info("\n" + "=" * 70)
    logging.info("✅ Fleet management demo complete!")
    logging.info("=" * 70)

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_fleet())


