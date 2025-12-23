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
from monorail_fleet import MonorailFleet, MonorailLine
from line_management import MonorailLineTracker

# Import new feature modules
try:
    from predictive_maintenance import PredictiveMaintenanceSystem, MaintenanceRecord
    from passenger_flow import PassengerFlowOptimizationSystem, PassengerData
    from energy_management import EnergyManagementSystem, EnergyConsumptionRecord
    from weather_adaptation import WeatherAdaptationSystem
    NEW_FEATURES_AVAILABLE = True
except ImportError as e:
    logging.warning(f"New features not available: {e}")
    NEW_FEATURES_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

app = FastAPI(title="WDW Monorail API", version="2.0")

# Initialize fleet with all 14 monorails
fleet = MonorailFleet()

# Initialize new feature systems
predictive_maintenance = PredictiveMaintenanceSystem() if NEW_FEATURES_AVAILABLE else None
passenger_flow = PassengerFlowOptimizationSystem() if NEW_FEATURES_AVAILABLE else None
energy_management = EnergyManagementSystem() if NEW_FEATURES_AVAILABLE else None
weather_adaptation = WeatherAdaptationSystem() if NEW_FEATURES_AVAILABLE else None

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

@app.get("/fleet")
async def get_fleet():
    """Get all 14 monorails"""
    result = {}
    for monorail_id, train in fleet.get_fleet().items():
        result[monorail_id] = {
            "name": train.color,
            "train_number": train.train_number,
            "operational": train.operational,
            "line": train.line.value if train.line else None,
            "status": train.status
        }
    return result

@app.get("/fleet/active")
async def get_active_fleet():
    """Get only active monorails (12)"""
    result = {}
    for monorail_id, train in fleet.get_active_fleet().items():
        result[monorail_id] = {
            "name": train.color,
            "train_number": train.train_number,
            "operational": True,
            "line": train.line.value if train.line else None
        }
    return result

@app.get("/fleet/retired")
async def get_retired_fleet():
    """Get retired monorails (2) - Post-2009 accident"""
    result = {}
    for monorail_id, train in fleet.get_retired_fleet().items():
        result[monorail_id] = {
            "name": train.color,
            "train_number": train.train_number,
            "operational": False,
            "retired_year": 2009,
            "retired_reason": "Monorail accident"
        }
    return result

@app.get("/fleet/summary")
async def get_fleet_summary():
    """Get fleet summary statistics"""
    return fleet.get_fleet_summary()

@app.get("/fleet/by-line/{line_id}")
async def get_fleet_by_line(line_id: str):
    """Get all active monorails assigned to a specific line"""
    try:
        line = MonorailLine(line_id)
        result = {}
        for monorail_id, train in fleet.get_monorails_by_line(line).items():
            result[monorail_id] = {
                "name": train.color,
                "train_number": train.train_number,
                "line": train.line.value if train.line else None
            }
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid line: {line_id}")

@app.post("/monorail/{monorail_id}/assign-line")
async def assign_monorail_to_line(monorail_id: str, line: str):
    """Assign a monorail to a line"""
    try:
        line_enum = MonorailLine(line)
        success = fleet.assign_to_line(monorail_id, line_enum)
        if success:
            train = fleet.get_monorail(monorail_id)
            return {
                "monorail_id": monorail_id,
                "color": train.color,
                "train_number": train.train_number,
                "line": line,
                "status": "assigned"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Cannot assign {monorail_id} to line")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid line: {line}")

@app.get("/monorail/{monorail_id}")
async def get_monorail(monorail_id: str):
    """Get specific monorail details"""
    train = fleet.get_monorail(monorail_id)
    if not train:
        raise HTTPException(status_code=404, detail="Monorail not found")
    return {
        "monorail_id": monorail_id,
        "name": train.color,
        "train_number": train.train_number,
        "operational": train.operational,
        "line": train.line.value if train.line else None,
        "status": train.status,
        "position": train.position,
        "speed": train.speed
    }

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

# NEW FEATURE ENDPOINTS

@app.get("/maintenance/predictive")
async def get_predictive_maintenance():
    """Get predictive maintenance status for all monorails"""
    if not NEW_FEATURES_AVAILABLE or not predictive_maintenance:
        raise HTTPException(status_code=503, detail="Predictive maintenance feature not available")
    
    results = {}
    for monorail_id in fleet.get_active_fleet().keys():
        prediction = predictive_maintenance.predict_maintenance(monorail_id)
        results[monorail_id] = prediction
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "predictions": results
    }

@app.get("/maintenance/predictive/{monorail_id}")
async def get_monorail_maintenance_prediction(monorail_id: str):
    """Get predictive maintenance status for a specific monorail"""
    if not NEW_FEATURES_AVAILABLE or not predictive_maintenance:
        raise HTTPException(status_code=503, detail="Predictive maintenance feature not available")
    
    prediction = predictive_maintenance.predict_maintenance(monorail_id)
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "monorail_id": monorail_id,
        "prediction": prediction
    }

@app.get("/maintenance/history/{monorail_id}")
async def get_maintenance_history(monorail_id: str):
    """Get maintenance history for a monorail"""
    if not NEW_FEATURES_AVAILABLE or not predictive_maintenance:
        raise HTTPException(status_code=503, detail="Predictive maintenance feature not available")
    
    history = predictive_maintenance.get_maintenance_history(monorail_id)
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "monorail_id": monorail_id,
        "maintenance_history": [record.to_dict() for record in history]
    }

@app.post("/maintenance/record")
async def add_maintenance_record(record: Dict):
    """Add a new maintenance record"""
    if not NEW_FEATURES_AVAILABLE or not predictive_maintenance:
        raise HTTPException(status_code=503, detail="Predictive maintenance feature not available")
    
    try:
        maintenance_record = MaintenanceRecord(
            monorail_id=record["monorail_id"],
            maintenance_type=record["maintenance_type"],
            date=datetime.fromisoformat(record["date"]),
            component=record["component"],
            severity=record["severity"],
            description=record["description"],
            parts_replaced=record.get("parts_replaced", [])
        )
        
        predictive_maintenance.add_maintenance_record(maintenance_record)
        return {
            "status": "success",
            "message": "Maintenance record added",
            "record_id": f"{record['monorail_id']}_{datetime.now().timestamp()}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid record data: {str(e)}")

@app.get("/passenger/flow")
async def get_passenger_flow():
    """Get current passenger flow analysis"""
    if not NEW_FEATURES_AVAILABLE or not passenger_flow:
        raise HTTPException(status_code=503, detail="Passenger flow feature not available")
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "crowding_status": passenger_flow.get_current_crowding(),
        "optimization_recommendations": passenger_flow.get_optimization_recommendations()
    }

@app.get("/passenger/stations")
async def get_passenger_data_by_station():
    """Get passenger data for all stations"""
    if not NEW_FEATURES_AVAILABLE or not passenger_flow:
        raise HTTPException(status_code=503, detail="Passenger flow feature not available")
    
    stations_data = {}
    for station in passenger_flow.analyzer.stations:
        data = passenger_flow.analyzer.get_passenger_counts_by_station(station)
        stations_data[station] = [d.to_dict() for d in data]
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "stations": stations_data
    }

@app.post("/passenger/data")
async def add_passenger_data(data: Dict):
    """Add passenger count data"""
    if not NEW_FEATURES_AVAILABLE or not passenger_flow:
        raise HTTPException(status_code=503, detail="Passenger flow feature not available")
    
    try:
        passenger_data = PassengerData(
            station=data["station"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            passengers_in=data["passengers_in"],
            passengers_out=data["passengers_out"]
        )
        
        passenger_flow.add_real_time_data(
            passenger_data.station,
            passenger_data.passengers_in,
            passenger_data.passengers_out
        )
        
        return {
            "status": "success",
            "message": "Passenger data added"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid passenger data: {str(e)}")

@app.get("/energy/status")
async def get_energy_status():
    """Get current energy management status"""
    if not NEW_FEATURES_AVAILABLE or not energy_management:
        raise HTTPException(status_code=503, detail="Energy management feature not available")
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "energy_data": energy_management.get_energy_dashboard_data()
    }

@app.post("/energy/data")
async def add_energy_data(data: Dict):
    """Add energy consumption data"""
    if not NEW_FEATURES_AVAILABLE or not energy_management:
        raise HTTPException(status_code=503, detail="Energy management feature not available")
    
    try:
        energy_record = energy_management.add_energy_data(
            monorail_id=data["monorail_id"],
            power_consumption=data["power_consumption"],
            speed=data["speed"],
            passengers=data["passengers"],
            line=data["line"]
        )
        
        return {
            "status": "success",
            "message": "Energy data added",
            "record": energy_record.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid energy data: {str(e)}")

@app.get("/energy/report")
async def get_energy_report(days: int = 7):
    """Get energy savings report"""
    if not NEW_FEATURES_AVAILABLE or not energy_management:
        raise HTTPException(status_code=503, detail="Energy management feature not available")
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "report": energy_management.get_energy_savings_report(days)
    }

@app.get("/weather/current")
async def get_current_weather():
    """Get current weather and adaptation status"""
    if not NEW_FEATURES_AVAILABLE or not weather_adaptation:
        raise HTTPException(status_code=503, detail="Weather adaptation feature not available")
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "weather_adaptation": weather_adaptation.get_current_weather_adaptation()
    }

@app.get("/weather/forecast")
async def get_weather_forecast(hours: int = 6):
    """Get weather forecast impact analysis"""
    if not NEW_FEATURES_AVAILABLE or not weather_adaptation:
        raise HTTPException(status_code=503, detail="Weather adaptation feature not available")
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "forecast": weather_adaptation.get_weather_forecast_impact(hours)
    }

@app.get("/system/health")
async def get_system_health():
    """Get overall system health including all subsystems"""
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "subsystems": {
            "fleet_management": {
                "status": "operational",
                "active_trains": len(fleet.get_active_fleet()),
                "retired_trains": len(fleet.get_retired_fleet())
            },
            "predictive_maintenance": {
                "status": "operational" if NEW_FEATURES_AVAILABLE and predictive_maintenance else "unavailable",
                "monorails_monitored": len(predictive_maintenance.health_monitors) if predictive_maintenance else 0
            },
            "passenger_flow": {
                "status": "operational" if NEW_FEATURES_AVAILABLE and passenger_flow else "unavailable",
                "stations_monitored": len(passenger_flow.analyzer.stations) if passenger_flow else 0
            },
            "energy_management": {
                "status": "operational" if NEW_FEATURES_AVAILABLE and energy_management else "unavailable",
                "monorails_monitored": len(energy_management.monitor.real_time_data) if energy_management else 0
            },
            "weather_adaptation": {
                "status": "operational" if NEW_FEATURES_AVAILABLE and weather_adaptation else "unavailable",
                "current_weather": weather_adaptation.weather_adapter.current_weather.to_dict() if weather_adaptation and weather_adaptation.weather_adapter.current_weather else None
            }
        }
    }
    
    # Calculate overall status
    operational_count = sum(1 for sub in health_status["subsystems"].values() if sub["status"] == "operational")
    total_subsystems = len(health_status["subsystems"])
    
    if operational_count == total_subsystems:
        health_status["overall_status"] = "fully_operational"
    elif operational_count >= total_subsystems * 0.75:
        health_status["overall_status"] = "partially_operational"
    else:
        health_status["overall_status"] = "degraded"
    
    return {
        "status": "success",
        "health": health_status
    }

@app.websocket("/ws/monorail")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # Enhanced state with new feature data
            enhanced_state = monorail_state.copy()
            
            if NEW_FEATURES_AVAILABLE:
                enhanced_state["predictive_maintenance"] = {
                    "status": "available",
                    "last_update": datetime.now().isoformat()
                }
                enhanced_state["passenger_flow"] = {
                    "status": "available",
                    "last_update": datetime.now().isoformat()
                }
                enhanced_state["energy_management"] = {
                    "status": "available",
                    "last_update": datetime.now().isoformat()
                }
                enhanced_state["weather_adaptation"] = {
                    "status": "available",
                    "last_update": datetime.now().isoformat()
                }
            
            await websocket.send_json(enhanced_state)
            await asyncio.sleep(1)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)




