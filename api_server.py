#!/usr/bin/env python3
"""
WDW Monorail API Server
REST API for monorail control & monitoring
"""

import json
import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

app = FastAPI(title="WDW Monorail API", version="1.0")

# Simulated monorail state
monorail_state = {
    "status": "idle",
    "current_station": None,
    "next_station": None,
    "speed": 0,
    "position": 0,
    "passengers": 0,
    "is_running": False,
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

