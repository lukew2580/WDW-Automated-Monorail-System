# WDW Monorail API Documentation

## Overview

The WDW Monorail API provides complete control and monitoring of Disney monorail trains with full line awareness. Each monorail knows which of the three Disney World lines it operates on:

- **Resort Line** (Red) - Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC
- **Express Line** (Blue) - Direct route: TTC ↔ Magic Kingdom (no resort stops)
- **Express to Epcot** (Gold/Yellow) - Direct route: TTC ↔ Epcot

## Base URL

```
http://127.0.0.1:8002
```

## Line Management Endpoints

### Get All Lines

```bash
GET /lines
```

Returns information about all three WDW monorail lines.

**Response:**
```json
{
  "resort": {
    "name": "Resort Line",
    "color": "#FF0000",
    "total_distance": 11000,
    "description": "Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC",
    "stations": ["ttr", "grand_floridian", "polynesian", "contemporary", "mk"]
  },
  "express": {
    "name": "Express Line",
    "color": "#0000FF",
    "total_distance": 14000,
    "description": "Express: TTC ↔ Magic Kingdom (no resort stops)",
    "stations": ["ttr", "mk"]
  },
  "express_epcot": {
    "name": "Express to Epcot",
    "color": "#FFB81C",
    "total_distance": 12000,
    "description": "Express: TTC ↔ Epcot (direct line)",
    "stations": ["ttr", "epcot"]
  }
}
```

### Get Line Details

```bash
GET /lines/{line_id}
```

Get detailed information about a specific line.

**Parameters:**
- `line_id` - Line identifier: `resort`, `express`, or `express_epcot`

**Example:**
```bash
curl http://127.0.0.1:8002/lines/resort
```

**Response:**
```json
{
  "line_id": "resort",
  "name": "Resort Line",
  "color": "#FF0000",
  "total_distance": 11000,
  "description": "Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC",
  "stations": ["ttr", "grand_floridian", "polynesian", "contemporary", "mk"]
}
```

### Assign Monorail to Line

```bash
POST /monorail/{monorail_id}/assign-line?line={line_id}
```

Assign a specific monorail to a WDW line.

**Parameters:**
- `monorail_id` - Unique monorail identifier (e.g., `monorail-mk-1`)
- `line` - Line to assign: `resort`, `express`, or `express_epcot`

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
    "monorail_id": "monorail-mk-1",
    "line": "resort",
    "line_name": "Resort Line",
    "line_color": "#FF0000",
    "current_station": null,
    "next_station": null,
    "route_description": "Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC",
    "is_valid": true,
    "total_route_distance": 11000,
    "line_switches": 1
  }
}
```

### Get Monorail Line Status

```bash
GET /monorail/{monorail_id}/line-status
```

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
  "line": "resort",
  "line_name": "Resort Line",
  "line_color": "#FF0000",
  "current_station": "ttr",
  "next_station": "grand_floridian",
  "route_description": "Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC",
  "is_valid": true,
  "total_route_distance": 11000,
  "line_switches": 1
}
```

## Control Endpoints

### Start Monorail

```bash
POST /monorail/start
```

Start the monorail.

**Response:**
```json
{
  "status": "started"
}
```

### Stop Monorail

```bash
POST /monorail/stop
```

Stop the monorail.

**Response:**
```json
{
  "status": "stopped"
}
```

### Set Speed

```bash
POST /monorail/speed/{speed}
```

Set monorail speed (0-100%).

**Parameters:**
- `speed` - Speed percentage (0-100)

**Example:**
```bash
curl -X POST http://127.0.0.1:8002/monorail/speed/75
```

**Response:**
```json
{
  "speed": 75
}
```

### Go to Station

```bash
POST /monorail/go-to-station/{station}
```

Route monorail to a specific station.

**Parameters:**
- `station` - Station name from the route

**Example:**
```bash
curl -X POST http://127.0.0.1:8002/monorail/go-to-station/magic_kingdom
```

**Response:**
```json
{
  "next_station": "magic_kingdom",
  "status": "routing"
}
```

### Get Current Status

```bash
GET /monorail/status
```

Get the current status of the monorail system.

**Response:**
```json
{
  "status": "running",
  "current_station": "magic_kingdom",
  "next_station": "epcot",
  "speed": 75,
  "position": 5000,
  "passengers": 45,
  "is_running": true,
  "line": "express",
  "line_name": "Express Line"
}
```

### Get Route

```bash
GET /monorail/route
```

Get the full monorail route.

**Response:**
```json
{
  "route": [
    "magic_kingdom",
    "epcot",
    "hollywood_studios",
    "animal_kingdom",
    "ttr"
  ]
}
```

## Real-Time Updates

### WebSocket Connection

```bash
ws://127.0.0.1:8002/ws/monorail
```

Connect via WebSocket for real-time status updates. The server sends the complete monorail state every second.

**Example (JavaScript):**
```javascript
const ws = new WebSocket('ws://127.0.0.1:8002/ws/monorail');
ws.onmessage = (event) => {
  const status = JSON.parse(event.data);
  console.log('Monorail Status:', status);
};
```

## Complete Example Workflow

```bash
# 1. Check available lines
curl http://127.0.0.1:8002/lines

# 2. Assign monorail to Resort Line
curl -X POST "http://127.0.0.1:8002/monorail/train-1/assign-line?line=resort"

# 3. Check the line assignment
curl http://127.0.0.1:8002/monorail/train-1/line-status

# 4. Start the monorail
curl -X POST http://127.0.0.1:8002/monorail/start

# 5. Set speed to 80%
curl -X POST http://127.0.0.1:8002/monorail/speed/80

# 6. Route to Grand Floridian
curl -X POST http://127.0.0.1:8002/monorail/go-to-station/grand_floridian

# 7. Monitor status
curl http://127.0.0.1:8002/monorail/status

# 8. Stop the monorail
curl -X POST http://127.0.0.1:8002/monorail/stop
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include a detail message:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Station Reference

### Resort Line Stations
- `ttr` - Transportation & Ticket Center
- `grand_floridian` - Grand Floridian Resort
- `polynesian` - Polynesian Village Resort
- `contemporary` - Contemporary Resort
- `mk` - Magic Kingdom

### Express Line Stations
- `ttr` - Transportation & Ticket Center
- `mk` - Magic Kingdom

### Express to Epcot Stations
- `ttr` - Transportation & Ticket Center
- `epcot` - Epcot

---

*Last Updated: 2025-12-15*
*Version: 2.0*

