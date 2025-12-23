# WDW Monorail API Documentation

The WDW Monorail API provides complete control and monitoring of Disney monorail trains with full line awareness. Each monorail knows which of the three Disney World lines it operates on:

- **Resort Line**: TTC ↔ Poly ↔ GF ↔ MK
- **Express Line**: TTC ↔ MK ↔ Epcot ↔ HS  
- **Express to Epcot**: TTC ↔ Epcot (direct)

## Base URL

```
http://127.0.0.1:8002
```

## Authentication

No authentication required for local development. For production deployment, implement appropriate authentication mechanisms.

## API Endpoints

### Fleet Management

#### GET /fleet
Returns information about all 14 monorails (12 operational + 2 historic).

**Response:**
```json
{
  "monorail_red": {
    "name": "Red",
    "train_number": 1,
    "operational": true,
    "line": "resort",
    "status": "operational"
  },
  "monorail_blue": {
    "name": "Blue",
    "train_number": 5,
    "operational": true,
    "line": "express",
    "status": "operational"
  }
}
```

#### GET /fleet/active
Returns only the 12 operational monorails.

**Response:** Similar to /fleet but only operational trains.

#### GET /fleet/retired
Returns the 2 retired monorails (post-2009 accident).

**Response:**
```json
{
  "monorail_white": {
    "name": "White",
    "train_number": 13,
    "operational": false,
    "retired_year": 2009,
    "retired_reason": "Monorail accident"
  }
}
```

#### GET /fleet/summary
Returns fleet summary statistics.

**Response:**
```json
{
  "total_monorails": 14,
  "operational": 12,
  "retired": 2,
  "by_line": {
    "resort": 4,
    "express": 6,
    "epcot_express": 2
  }
}
```

### Monorail Control

#### POST /monorail/start
Start the monorail system.

**Response:**
```json
{"status": "started"}
```

#### POST /monorail/stop
Stop the monorail system.

**Response:**
```json
{"status": "stopped"}
```

#### POST /monorail/speed/{speed}
Set monorail speed (0-100%).

**Parameters:**
- `speed` - Speed percentage (0-100)

**Response:**
```json
{"speed": 75}
```

#### POST /monorail/go-to-station/{station}
Route monorail to a specific station.

**Parameters:**
- `station` - Destination station (e.g., "magic_kingdom")

**Response:**
```json
{"next_station": "magic_kingdom", "status": "routing"}
```

### Line Management

#### GET /lines
Returns information about all three WDW monorail lines.

**Response:**
```json
{
  "resort": {
    "name": "Resort Line",
    "color": "blue",
    "total_distance": 7.1,
    "description": "Connects TTC with Magic Kingdom resorts",
    "stations": ["ttc", "poly", "gf", "mk"]
  }
}
```

#### GET /lines/{line_id}
Get detailed information about a specific line.

**Parameters:**
- `line_id` - Line identifier (resort, express, epcot_express)

**Response:** Detailed line information including stations and distances.

#### POST /monorail/{monorail_id}/assign-line?line={line_id}
Assign a specific monorail to a WDW line.

**Parameters:**
- `monorail_id` - Unique monorail identifier (e.g., `monorail-mk-1`)
- `line` - Line identifier (resort, express, epcot_express)

**Example:**
```bash
curl -X POST "http://127.0.0.1:8002/monorail/monorail-mk-1/assign-line?line=resort"
```

**Response:**
```json
{
  "monorail_id": "monorail-mk-1",
  "line": "resort",
  "status": "assigned",
  "line_info": {
    "current_line": "resort",
    "stations": ["ttc", "poly", "gf", "mk"],
    "next_station": "poly"
  }
}
```

#### GET /monorail/{monorail_id}/line-status
Get the current line and route information for a specific monorail.

**Parameters:**
- `monorail_id` - Unique monorail identifier

**Example:**
```bash
curl http://127.0.0.1:8002/monorail/monorail-mk-1/line-status
```

**Response:**
```json
{
  "monorail_id": "monorail-mk-1",
  "current_line": "resort",
  "current_station": "ttc",
  "next_station": "poly",
  "direction": "forward",
  "speed": 30,
  "passengers": 180
}
```

### System Status

#### GET /monorail/status
Get the current status of the monorail system.

**Response:**
```json
{
  "status": "running",
  "current_station": "ttc",
  "next_station": "poly",
  "speed": 30,
  "position": 1500,
  "passengers": 180,
  "is_running": true,
  "line": "resort",
  "line_name": "Resort Line",
  "route": ["ttc", "poly", "gf", "mk"]
}
```

#### GET /monorail/route
Get the full monorail route.

**Response:**
```json
{
  "route": ["ttc", "poly", "gf", "mk"]
}
```

### NEW: Predictive Maintenance Endpoints

#### GET /maintenance/predictive
Get predictive maintenance status for all monorails.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "predictions": {
    "monorail_red": {
      "prediction": "no_maintenance",
      "confidence": 0.85,
      "health_score": 88.2,
      "recommendation": "System operating normally"
    }
  }
}
```

#### GET /maintenance/predictive/{monorail_id}
Get predictive maintenance status for a specific monorail.

**Parameters:**
- `monorail_id` - Monorail identifier

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "monorail_id": "monorail_red",
  "prediction": {
    "prediction": "no_maintenance",
    "confidence": 0.85,
    "health_score": 88.2,
    "recommendation": "System operating normally",
    "last_maintenance": "2025-12-15T10:30:00",
    "metrics": {
      "motor_temperature": 72.5,
      "bearing_vibration": 1.1,
      "braking_distance": 205.0
    }
  }
}
```

#### GET /maintenance/history/{monorail_id}
Get maintenance history for a specific monorail.

**Parameters:**
- `monorail_id` - Monorail identifier

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "monorail_id": "monorail_red",
  "maintenance_history": [
    {
      "monorail_id": "monorail_red",
      "maintenance_type": "preventive",
      "date": "2025-12-15T10:30:00",
      "component": "motor",
      "severity": 2,
      "description": "Routine motor inspection and lubrication",
      "parts_replaced": []
    }
  ]
}
```

#### POST /maintenance/record
Add a new maintenance record.

**Request Body:**
```json
{
  "monorail_id": "monorail_red",
  "maintenance_type": "preventive",
  "date": "2025-12-20T10:30:00",
  "component": "brakes",
  "severity": 2,
  "description": "Brake pad inspection and adjustment",
  "parts_replaced": ["brake_pads"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Maintenance record added",
  "record_id": "monorail_red_1703082600.0"
}
```

### NEW: Passenger Flow Endpoints

#### GET /passenger/flow
Get current passenger flow analysis.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "crowding_status": {
    "TTC": {
      "current_passengers": 185,
      "level": "medium",
      "last_updated": "2025-12-20T21:45:00"
    },
    "MK": {
      "current_passengers": 420,
      "level": "high",
      "last_updated": "2025-12-20T21:45:00"
    }
  },
  "optimization_recommendations": {
    "route_optimization": {
      "resort": ["TTC", "Poly", "GF", "MK"],
      "express": ["TTC", "MK", "Epcot", "HS"]
    },
    "train_allocation": {
      "resort": 4,
      "express": 5,
      "epcot_express": 2
    }
  }
}
```

#### GET /passenger/stations
Get passenger data for all stations.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "stations": {
    "TTC": [
      {
        "station": "TTC",
        "timestamp": "2025-12-20T21:45:00",
        "passengers_in": 85,
        "passengers_out": 60
      }
    ]
  }
}
```

#### POST /passenger/data
Add passenger count data.

**Request Body:**
```json
{
  "station": "MK",
  "timestamp": "2025-12-20T21:45:00",
  "passengers_in": 210,
  "passengers_out": 185
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Passenger data added"
}
```

### NEW: Energy Management Endpoints

#### GET /energy/status
Get current energy management status.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "energy_data": {
    "current_power_usage": {
      "monorail_red": 115.5,
      "monorail_blue": 120.2
    },
    "energy_efficiency": {
      "monorail_red": 8.1,
      "monorail_blue": 7.8
    },
    "optimization_recommendations": {
      "current_total_power_kw": 235.7,
      "average_efficiency": 7.9,
      "savings_opportunities": [],
      "potential_total_savings_kw": 0.0
    }
  }
}
```

#### POST /energy/data
Add energy consumption data.

**Request Body:**
```json
{
  "monorail_id": "monorail_red",
  "power_consumption": 115.5,
  "speed": 30.0,
  "passengers": 280,
  "line": "express"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Energy data added",
  "record": {
    "monorail_id": "monorail_red",
    "timestamp": "2025-12-20T21:50:00",
    "power_consumption": 115.5,
    "speed": 30.0,
    "passengers": 280,
    "line": "express",
    "efficiency_score": 8.1
  }
}
```

#### GET /energy/report?days=7
Get energy savings report for the specified number of days.

**Parameters:**
- `days` - Number of days to include in report (default: 7)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "report": {
    "period_days": 7,
    "total_energy_consumption_kwh": 12500.5,
    "average_efficiency_score": 8.2,
    "potential_savings_kwh": 1875.1,
    "potential_savings_percentage": 15.0,
    "top_opportunities": [],
    "energy_consumption_by_line": {
      "resort": 4200.2,
      "express": 5800.8,
      "epcot_express": 2500.5
    }
  }
}
```

### NEW: Weather Adaptation Endpoints

#### GET /weather/current
Get current weather and adaptation status.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "weather_adaptation": {
    "current_weather": {
      "temperature": 78.5,
      "humidity": 65.0,
      "wind_speed": 12.3,
      "wind_direction": 180.0,
      "precipitation": 0.0,
      "visibility": 10.0,
      "conditions": "partly cloudy",
      "timestamp": "2025-12-20T21:45:00",
      "severity": "normal"
    },
    "speed_adjustment_factor": 1.0,
    "safety_recommendations": {
      "recommendations": ["Normal operations - monitor weather conditions"],
      "severity": "normal",
      "current_conditions": "partly cloudy",
      "wind_speed": 12.3,
      "precipitation": 0.0,
      "visibility": 10.0
    },
    "route_adjustments": {
      "adjustments": [],
      "severity": "normal"
    },
    "weather_alerts": [],
    "last_updated": "2025-12-20T21:50:00"
  }
}
```

#### GET /weather/forecast?hours=6
Get weather forecast impact analysis.

**Parameters:**
- `hours` - Number of hours ahead to forecast (default: 6)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-12-20T21:50:00",
  "forecast": {
    "forecast_period_hours": 6,
    "predicted_conditions": "partly cloudy",
    "predicted_impact": "no significant impact expected",
    "recommended_preparations": ["Normal operations - monitor weather conditions"],
    "confidence": "medium"
  }
}
```

### NEW: System Health Endpoint

#### GET /system/health
Get overall system health including all subsystems.

**Response:**
```json
{
  "status": "success",
  "health": {
    "timestamp": "2025-12-20T21:50:00",
    "overall_status": "fully_operational",
    "subsystems": {
      "fleet_management": {
        "status": "operational",
        "active_trains": 12,
        "retired_trains": 2
      },
      "predictive_maintenance": {
        "status": "operational",
        "monorails_monitored": 12
      },
      "passenger_flow": {
        "status": "operational",
        "stations_monitored": 6
      },
      "energy_management": {
        "status": "operational",
        "monorails_monitored": 12
      },
      "weather_adaptation": {
        "status": "operational",
        "current_weather": {
          "temperature": 78.5,
          "conditions": "partly cloudy",
          "severity": "normal"
        }
      }
    }
  }
}
```

### WebSocket Endpoint

#### ws://127.0.0.1:8002/ws/monorail
Connect via WebSocket for real-time status updates. The server sends the complete monorail state every second.

**Example JavaScript:**
```javascript
const ws = new WebSocket('ws://127.0.0.1:8002/ws/monorail');

ws.onmessage = function(event) {
    const state = JSON.parse(event.data);
    console.log('Current state:', state);
    // Update your UI with the real-time data
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

## Usage Examples

### 1. Get Fleet Information
```bash
curl http://127.0.0.1:8002/fleet
```

### 2. Assign monorail to Resort Line
```bash
curl -X POST "http://127.0.0.1:8002/monorail/train-1/assign-line?line=resort"
```

### 3. Check line assignment
```bash
curl http://127.0.0.1:8002/monorail/train-1/line-status
```

### 4. Start the monorail
```bash
curl -X POST http://127.0.0.1:8002/monorail/start
```

### 5. Set speed to 80%
```bash
curl -X POST http://127.0.0.1:8002/monorail/speed/80
```

### 6. Route to Magic Kingdom
```bash
curl -X POST http://127.0.0.1:8002/monorail/go-to-station/magic_kingdom
```

### 7. Check current status
```bash
curl http://127.0.0.1:8002/monorail/status
```

### 8. Stop the monorail
```bash
curl -X POST http://127.0.0.1:8002/monorail/stop
```

### NEW: 9. Check predictive maintenance
```bash
curl http://127.0.0.1:8002/maintenance/predictive/monorail_red
```

### NEW: 10. Get passenger flow analysis
```bash
curl http://127.0.0.1:8002/passenger/flow
```

### NEW: 11. Check energy status
```bash
curl http://127.0.0.1:8002/energy/status
```

### NEW: 12. Get weather adaptation status
```bash
curl http://127.0.0.1:8002/weather/current
```

### NEW: 13. Check system health
```bash
curl http://127.0.0.1:8002/system/health
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Feature not available

Error responses include a JSON body with details:

```json
{
  "detail": "Invalid line: invalid_line_name"
}
```

## Rate Limiting

For production deployment, implement rate limiting to prevent abuse. The current implementation has no rate limits for local development.

## Versioning

The API follows semantic versioning. Current version: 2.0

- Major version changes indicate breaking changes
- Minor version changes indicate new features
- Patch version changes indicate bug fixes

## Changelog

### Version 2.0 (Current)
- Added predictive maintenance endpoints
- Added passenger flow optimization endpoints
- Added energy management endpoints
- Added weather adaptation endpoints
- Added system health endpoint
- Enhanced existing endpoints with new feature integration

### Version 1.0
- Initial release with basic fleet management
- Monorail control endpoints
- Line management endpoints
- Real-time WebSocket updates

## Deprecation Policy

Deprecated endpoints will be marked in the documentation and maintained for at least 6 months before removal.

## Support

For API support, refer to the comprehensive documentation or contact the development team.

## Examples in Different Languages

### Python
```python
import requests

# Get fleet information
response = requests.get("http://127.0.0.1:8002/fleet")
fleet_data = response.json()
print(fleet_data)

# Assign monorail to line
assign_response = requests.post(
    "http://127.0.0.1:8002/monorail/monorail_red/assign-line",
    params={"line": "resort"}
)
print(assign_response.json())
```

### JavaScript
```javascript
// Using fetch API
async function getFleet() {
    const response = await fetch('http://127.0.0.1:8002/fleet');
    const data = await response.json();
    console.log(data);
    return data;
}

async function assignToLine(monorailId, line) {
    const response = await fetch(
        `http://127.0.0.1:8002/monorail/${monorailId}/assign-line?line=${line}`,
        { method: 'POST' }
    );
    const data = await response.json();
    console.log(data);
    return data;
}
```

### cURL
```bash
# Get all lines information
curl http://127.0.0.1:8002/lines

# Get specific monorail details
curl http://127.0.0.1:8002/monorail/monorail_red

# Start monorail
curl -X POST http://127.0.0.1:8002/monorail/start
```

## Best Practices

1. **Error Handling**: Always handle potential API errors in your client code
2. **Rate Limiting**: Implement client-side rate limiting for production use
3. **Caching**: Cache responses where appropriate to reduce API calls
4. **Authentication**: Implement proper authentication for production deployment
5. **HTTPS**: Always use HTTPS in production environments
6. **Input Validation**: Validate all inputs before sending to the API
7. **Retry Logic**: Implement retry logic for transient failures
8. **Logging**: Log API interactions for debugging and monitoring

## Troubleshooting

### Common Issues

**Connection refused**:
- Ensure the API server is running
- Check the server port (default: 8002)
- Verify no firewall is blocking the connection

**Invalid line errors**:
- Use valid line identifiers: resort, express, epcot_express
- Check for typos in line names

**Monorail not found**:
- Verify the monorail_id exists in the fleet
- Check the fleet endpoint for valid monorail IDs

**Feature not available**:
- Ensure all dependencies are installed
- Check that new feature modules are properly imported
- Verify the feature is enabled in the API server

### Debugging

Enable debug logging by setting the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

Check server logs for detailed error information.

## Performance Considerations

- The API is designed for real-time control with low latency
- WebSocket updates are sent every second for real-time monitoring
- Consider implementing client-side caching for frequently accessed data
- Use pagination for endpoints that return large datasets
- Optimize network usage by only requesting needed data

## Security Considerations

For production deployment:

1. **Authentication**: Implement JWT or OAuth2 authentication
2. **Authorization**: Implement role-based access control
3. **HTTPS**: Use TLS/SSL for all communications
4. **Input Validation**: Validate all API inputs
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **CORS**: Configure CORS properly for web clients
7. **Logging**: Implement comprehensive logging
8. **Monitoring**: Set up monitoring and alerting

## API Client Libraries

While no official client libraries are provided, the API follows RESTful conventions and can be used with any HTTP client library in your preferred programming language.

## Mobile API

For mobile applications, a separate mobile-optimized API is available on port 8003. Refer to the mobile API documentation for details on mobile-specific endpoints and authentication.

## WebSocket Best Practices

1. **Reconnection**: Implement automatic reconnection logic
2. **Heartbeat**: Use ping/pong frames to keep connection alive
3. **Error Handling**: Handle connection errors gracefully
4. **Message Processing**: Process messages efficiently to avoid backlog
5. **Connection Management**: Close connections properly when no longer needed

## API Evolution

The API will evolve over time with new features and improvements. Check this documentation regularly for updates and new endpoints.

## Feedback

Provide feedback on the API design, documentation, or suggest new features by submitting issues or pull requests to the project repository.

---

**Last Updated**: 2025-12-20  
**API Version**: 2.0  
**Documentation Version**: 3.0


