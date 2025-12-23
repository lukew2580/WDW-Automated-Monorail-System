#!/usr/bin/env python3
"""
Simple test API server for dashboard testing
"""

import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import time

class MonorailAPIHandler(BaseHTTPRequestHandler):
    fleet_state = {
        "trains": {
            "red": {"position": 1000, "speed": 25, "passengers": 45, "status": "in_transit", "line": "express"},
            "orange": {"position": 2500, "speed": 30, "passengers": 38, "status": "in_transit", "line": "resort"},
            "yellow": {"position": 5000, "speed": 20, "passengers": 52, "status": "stopped", "line": "epcot"},
            "green": {"position": 1500, "speed": 28, "passengers": 42, "status": "in_transit", "line": "resort"},
            "blue": {"position": 3200, "speed": 32, "passengers": 48, "status": "in_transit", "line": "express"},
            "purple": {"position": 4800, "speed": 15, "passengers": 35, "status": "boarding", "line": "epcot"},
            "pink": {"position": 2000, "speed": 26, "passengers": 41, "status": "in_transit", "line": "express"},
            "coral": {"position": 6000, "speed": 22, "passengers": 50, "status": "in_transit", "line": "resort"},
            "teal": {"position": 800, "speed": 29, "passengers": 46, "status": "in_transit", "line": "express"},
            "silver": {"position": 3500, "speed": 24, "passengers": 44, "status": "in_transit", "line": "resort"},
            "gold": {"position": 5500, "speed": 31, "passengers": 47, "status": "in_transit", "line": "epcot"},
            "lime": {"position": 1200, "speed": 27, "passengers": 43, "status": "in_transit", "line": "resort"},
        },
        "lines": {
            "resort": {"status": "operational", "trains": 5},
            "express": {"status": "operational", "trains": 4},
            "epcot": {"status": "operational", "trains": 3},
        },
        "safety": {"status": "green", "collision_risk": False}
    }

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "timestamp": time.time()}).encode())
        
        elif self.path == "/fleet":
            # Update positions dynamically
            for train in self.fleet_state["trains"].values():
                train["position"] = (train["position"] + random.randint(-200, 200)) % 10000
                train["speed"] = max(0, min(35, train["speed"] + random.randint(-3, 3)))
                train["passengers"] = max(0, min(60, train["passengers"] + random.randint(-5, 5)))
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self.fleet_state["trains"]).encode())
        
        elif self.path == "/lines":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self.fleet_state["lines"]).encode())
        
        elif self.path == "/safety/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self.fleet_state["safety"]).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8002), MonorailAPIHandler)
    print("✅ Test API server running on http://127.0.0.1:8002")
    server.serve_forever()

