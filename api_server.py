#!/usr/bin/env python3
"""
WDW Monorail API Server
REST API for monorail control & monitoring with line awareness
"""

import json
import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from datetime import datetime
from line_management import MonorailLine, MonorailLineTracker

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

app = FastAPI(title="WDW Monorail API", version="2.0")

# Monorail trackers by ID
monorail_trackers = {}

# Simulated monorail state
monorail_state = {
    "status": "idle",
    "current_station": None,
    "next_station": None,
    "speed": 0,
    "position": 0,
    "passengers": 0,
    "is_running": False,
    "line": None,
    "line_name": None,
    "route": [
        "magic_kingdom",
        "epcot", 
        "hollywood_studios",
        "animal_kingdom",
        "ttr"
    ]
}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# LINE MANAGEMENT ENDPOINTS

@app.post("/monorail/{monorail_id}/assign-line")
async def assign_monorail_line(monorail_id: str, line: str):
    """Assign a monorail to a specific WDW line"""
    try:
        line_enum = MonorailLine[line.upper().replace("-", "_")]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid line: {line}")
    
    if monorail_id not in monorail_trackers:
        monorail_trackers[monorail_id] = MonorailLineTracker(monorail_id)
    
    tracker = monorail_trackers[monorail_id]
    success = await tracker.set_line(line_enum)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to assign line")
    
    return {
        "monorail_id": monorail_id,
        "line": line_enum.value,
        "status": "assigned",
        "line_info": tracker.get_line_status()
    }

@app.get("/monorail/{monorail_id}/line-status")
async def get_line_status(monorail_id: str):
    """Get the current line and route information for a monorail"""
    if monorail_id not in monorail_trackers:
        raise HTTPException(status_code=404, detail=f"Monorail {monorail_id} not found")
    
    tracker = monorail_trackers[monorail_id]
    return tracker.get_line_status()

@app.get("/lines")
async def get_all_lines():
    """Get information about all WDW monorail lines"""
    from line_management import LineManager
    
    manager = LineManager()
    lines_info = {}
    
    for line in MonorailLine:
        route = manager.get_line_info(line)
        lines_info[line.value] = {
            "name": route.name,
            "color": route.color,
            "total_distance": route.total_distance,
            "description": route.description,
            "stations": [s.value for s in route.stations]
        }
    
    return lines_info

@app.get("/lines/{line_id}")
async def get_line_info(line_id: str):
    """Get detailed information about a specific line"""
    try:
        line_enum = MonorailLine[line_id.upper().replace("-", "_")]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Line not found: {line_id}")
    
    from line_management import LineManager
    manager = LineManager()
    route = manager.get_line_info(line_enum)
    
    return {
        "line_id": line_enum.value,
        "name": route.name,
        "color": route.color,
        "total_distance": route.total_distance,
        "description": route.description,
        "stations": [s.value for s in route.stations]
    }

@app.get("/monorail/status")
async def get_status():
    """Get current monorail status"""
    return monorail_state

@app.post("/monorail/start")
async def start_monorail():
    """Start the monorail"""
    monorail_state["is_running"] = True
    monorail_state["status"] = "running"
    monorail_state["speed"] = 10
    logging.info("Monorail started")
    return {"status": "started"}

@app.post("/monorail/stop")
async def stop_monorail():
    """Stop the monorail"""
    monorail_state["is_running"] = False
    monorail_state["status"] = "stopped"
    monorail_state["speed"] = 0
    logging.info("Monorail stopped")
    return {"status": "stopped"}

@app.post("/monorail/go-to-station/{station}")
async def go_to_station(station: str):
    """Route monorail to specific station"""
    if station not in monorail_state["route"]:
        raise HTTPException(status_code=400, detail="Invalid station")
    
    monorail_state["next_station"] = station
    monorail_state["is_running"] = True
    logging.info(f"Routing to {station}")
    return {"next_station": station, "status": "routing"}

@app.post("/monorail/speed/{speed}")
async def set_speed(speed: int):
    """Set monorail speed (0-100)"""
    if not 0 <= speed <= 100:
        raise HTTPException(status_code=400, detail="Speed must be 0-100")
    
    monorail_state["speed"] = speed
    logging.info(f"Speed set to {speed}%")
    return {"speed": speed}

@app.get("/monorail/route")
async def get_route():
    """Get full monorail route"""
    return {"route": monorail_state["route"]}

@app.websocket("/ws/monorail")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(monorail_state)
            await asyncio.sleep(1)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)


