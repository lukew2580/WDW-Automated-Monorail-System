#!/usr/bin/env python3
"""
WDW Monorail Mobile API

Mobile-optimized API endpoints and services for passenger information
and system monitoring via mobile applications.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import secrets
import hashlib
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)sZ %(levelname)s [MOBILE_API] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mobile_api.log")
    ]
)
logger = logging.getLogger(__name__)


# Security setup
security = HTTPBearer()


class MobileUser(BaseModel):
    """Represents a mobile app user"""
    user_id: str
    device_id: str
    api_key: str
    last_access: datetime
    preferences: Dict
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "device_id": self.device_id,
            "api_key": self.api_key,
            "last_access": self.last_access.isoformat(),
            "preferences": self.preferences
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            user_id=data["user_id"],
            device_id=data["device_id"],
            api_key=data["api_key"],
            last_access=datetime.fromisoformat(data["last_access"]),
            preferences=data.get("preferences", {})
        )


class MobileAPI:
    """Mobile API for WDW Monorail System"""
    
    def __init__(self):
        self.users: Dict[str, MobileUser] = {}  # user_id -> MobileUser
        self.sessions: Dict[str, str] = {}     # session_token -> user_id
        self.load_users()
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="WDW Monorail Mobile API",
            version="1.0",
            description="Mobile API for WDW Monorail System"
        )
        
        # Setup routes
        self._setup_routes()
        
    def load_users(self):
        """Load user data from file"""
        try:
            if os.path.exists("mobile_users.json"):
                with open("mobile_users.json", "r") as f:
                    data = json.load(f)
                    self.users = {user["user_id"]: MobileUser.from_dict(user) for user in data}
                logger.info(f"Loaded {len(self.users)} mobile users")
        except Exception as e:
            logger.error(f"Error loading mobile users: {e}")
    
    def save_users(self):
        """Save user data to file"""
        try:
            with open("mobile_users.json", "w") as f:
                json.dump([user.to_dict() for user in self.users.values()], f, indent=2)
            logger.info(f"Saved {len(self.users)} mobile users")
        except Exception as e:
            logger.error(f"Error saving mobile users: {e}")
    
    def generate_api_key(self) -> str:
        """Generate a secure API key"""
        return secrets.token_hex(32)
    
    def generate_session_token(self) -> str:
        """Generate a session token"""
        return secrets.token_hex(16)
    
    def authenticate_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> MobileUser:
        """Authenticate user based on API key or session token"""
        token = credentials.credentials
        
        # Check if it's a session token
        if token in self.sessions:
            user_id = self.sessions[token]
            if user_id in self.users:
                return self.users[user_id]
        
        # Check if it's an API key
        for user in self.users.values():
            if secrets.compare_digest(user.api_key, token):
                return user
        
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    def register_user(self, device_id: str, preferences: Dict = None) -> MobileUser:
        """Register a new mobile user"""
        user_id = f"user_{secrets.token_hex(8)}"
        api_key = self.generate_api_key()
        
        user = MobileUser(
            user_id=user_id,
            device_id=device_id,
            api_key=api_key,
            last_access=datetime.now(),
            preferences=preferences or {"notifications": True, "theme": "light"}
        )
        
        self.users[user_id] = user
        self.save_users()
        
        return user
    
    def create_session(self, user: MobileUser) -> str:
        """Create a new session for a user"""
        session_token = self.generate_session_token()
        self.sessions[session_token] = user.user_id
        
        # Update last access time
        user.last_access = datetime.now()
        self.save_users()
        
        return session_token
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.post("/register")
        async def register(device_id: str, preferences: Dict = None):
            """Register a new mobile device"""
            user = self.register_user(device_id, preferences)
            return {
                "status": "success",
                "user_id": user.user_id,
                "api_key": user.api_key,
                "message": "User registered successfully"
            }
        
        @self.app.post("/login")
        async def login(api_key: str):
            """Login with API key to get session token"""
            # Find user by API key
            user = None
            for u in self.users.values():
                if secrets.compare_digest(u.api_key, api_key):
                    user = u
                    break
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid API key")
            
            # Create session
            session_token = self.create_session(user)
            
            return {
                "status": "success",
                "session_token": session_token,
                "user_id": user.user_id,
                "expires_in": 86400  # 24 hours
            }
        
        @self.app.get("/status")
        async def get_status(user: MobileUser = Depends(self.authenticate_user)):
            """Get current monorail system status (mobile-optimized)"""
            # In a real implementation, this would fetch data from the main system
            # For this example, we'll return mock data
            
            return {
                "status": "operational",
                "timestamp": datetime.now().isoformat(),
                "lines": {
                    "resort": {
                        "status": "operational",
                        "trains": 4,
                        "next_departure": "2 min",
                        "crowding": "medium"
                    },
                    "express": {
                        "status": "operational",
                        "trains": 3,
                        "next_departure": "5 min",
                        "crowding": "low"
                    },
                    "epcot_express": {
                        "status": "operational",
                        "trains": 2,
                        "next_departure": "10 min",
                        "crowding": "low"
                    }
                },
                "alerts": [],
                "weather": {
                    "conditions": "partly cloudy",
                    "temperature": 78,
                    "impact": "none"
                }
            }
        
        @self.app.get("/stations")
        async def get_stations(user: MobileUser = Depends(self.authenticate_user)):
            """Get information about all stations"""
            # Mock station data
            stations = {
                "TTC": {
                    "name": "Transportation and Ticket Center",
                    "lines": ["resort", "express", "epcot_express"],
                    "facilities": ["parking", "ticketing", "restrooms", "food"],
                    "crowding": "medium",
                    "next_departures": {
                        "resort": "2 min",
                        "express": "5 min",
                        "epcot_express": "10 min"
                    }
                },
                "MK": {
                    "name": "Magic Kingdom",
                    "lines": ["resort", "express"],
                    "facilities": ["park entrance", "restrooms", "food", "shopping"],
                    "crowding": "high",
                    "next_departures": {
                        "resort": "3 min",
                        "express": "7 min"
                    }
                },
                "Epcot": {
                    "name": "Epcot",
                    "lines": ["express", "epcot_express"],
                    "facilities": ["park entrance", "restrooms", "food"],
                    "crowding": "medium",
                    "next_departures": {
                        "express": "8 min",
                        "epcot_express": "15 min"
                    }
                }
            }
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "stations": stations
            }
        
        @self.app.get("/station/{station_id}")
        async def get_station_details(station_id: str, user: MobileUser = Depends(self.authenticate_user)):
            """Get detailed information about a specific station"""
            # Mock detailed station data
            station_data = {
                "TTC": {
                    "name": "Transportation and Ticket Center",
                    "description": "Main hub for WDW monorail system",
                    "lines": ["resort", "express", "epcot_express"],
                    "facilities": {
                        "parking": {"available": True, "spaces": 5000},
                        "ticketing": {"available": True, "hours": "8:00 AM - 8:00 PM"},
                        "restrooms": {"available": True, "locations": ["main building", "near monorail platform"]},
                        "food": {"available": True, "options": ["quick service", "sit-down"]}
                    },
                    "monorail_info": {
                        "platforms": 3,
                        "accessibility": "full",
                        "staffing": "full time",
                        "security": "present"
                    },
                    "real_time": {
                        "crowding": "medium",
                        "wait_time": "5-10 minutes",
                        "next_departures": {
                            "resort": {"time": "2 min", "destination": "Poly", "crowding": "low"},
                            "express": {"time": "5 min", "destination": "MK", "crowding": "medium"},
                            "epcot_express": {"time": "10 min", "destination": "Epcot", "crowding": "low"}
                        }
                    }
                }
            }.get(station_id.upper(), None)
            
            if not station_data:
                raise HTTPException(status_code=404, detail="Station not found")
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "station": station_data
            }
        
        @self.app.get("/schedule")
        async def get_schedule(user: MobileUser = Depends(self.authenticate_user)):
            """Get current monorail schedule"""
            # Mock schedule data
            now = datetime.now()
            schedule = []
            
            for i in range(10):  # Next 10 departures
                departure_time = now + timedelta(minutes=5*i)
                schedule.append({
                    "departure_time": departure_time.isoformat(),
                    "line": "resort" if i % 2 == 0 else "express",
                    "origin": "TTC",
                    "destination": "MK" if i % 3 == 0 else "Epcot",
                    "estimated_arrival": (departure_time + timedelta(minutes=15)).isoformat(),
                    "crowding": "low" if i % 4 == 0 else "medium"
                })
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "schedule": schedule,
                "last_updated": datetime.now().isoformat()
            }
        
        @self.app.get("/alerts")
        async def get_alerts(user: MobileUser = Depends(self.authenticate_user)):
            """Get current alerts and notifications"""
            # Mock alerts - in real system, this would come from main system
            alerts = []
            
            # Example: Check if user has notifications enabled
            if user.preferences.get("notifications", True):
                # Mock some alerts based on time of day
                hour = datetime.now().hour
                if 8 <= hour <= 10:
                    alerts.append({
                        "id": "alert_1",
                        "type": "info",
                        "title": "Morning Rush",
                        "message": "Monorail system is experiencing higher than normal ridership. Please allow extra time.",
                        "timestamp": datetime.now().isoformat(),
                        "expiry": (datetime.now() + timedelta(hours=2)).isoformat(),
                        "severity": "low"
                    })
                
                # Weather alert example
                alerts.append({
                    "id": "alert_2",
                    "type": "weather",
                    "title": "Afternoon Showers Expected",
                    "message": "Light rain expected this afternoon. Monorail service will continue normally.",
                    "timestamp": datetime.now().isoformat(),
                    "expiry": (datetime.now() + timedelta(hours=6)).isoformat(),
                    "severity": "low"
                })
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "alerts": alerts,
                "unread_count": len(alerts)
            }
        
        @self.app.get("/user/preferences")
        async def get_preferences(user: MobileUser = Depends(self.authenticate_user)):
            """Get user preferences"""
            return {
                "status": "success",
                "preferences": user.preferences
            }
        
        @self.app.post("/user/preferences")
        async def update_preferences(preferences: Dict, user: MobileUser = Depends(self.authenticate_user)):
            """Update user preferences"""
            user.preferences.update(preferences)
            user.last_access = datetime.now()
            self.save_users()
            
            return {
                "status": "success",
                "message": "Preferences updated",
                "updated_preferences": user.preferences
            }
        
        @self.app.get("/user/favorites")
        async def get_favorites(user: MobileUser = Depends(self.authenticate_user)):
            """Get user favorite stations and routes"""
            # Mock favorites
            favorites = user.preferences.get("favorites", {
                "stations": ["MK", "Epcot"],
                "routes": ["express"],
                "notifications": {
                    "MK": ["departures", "crowding"],
                    "Epcot": ["departures"]
                }
            })
            
            return {
                "status": "success",
                "favorites": favorites
            }
        
        @self.app.post("/user/favorites")
        async def update_favorites(favorites: Dict, user: MobileUser = Depends(self.authenticate_user)):
            """Update user favorites"""
            if "favorites" not in user.preferences:
                user.preferences["favorites"] = {}
            
            user.preferences["favorites"].update(favorites)
            user.last_access = datetime.now()
            self.save_users()
            
            return {
                "status": "success",
                "message": "Favorites updated",
                "updated_favorites": user.preferences["favorites"]
            }
        
        @self.app.get("/stats")
        async def get_stats(user: MobileUser = Depends(self.authenticate_user)):
            """Get system statistics"""
            # Mock statistics
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "stats": {
                    "operational_trains": 12,
                    "total_passengers_today": 18500,
                    "on_time_performance": 97.5,
                    "average_wait_time": "7 minutes",
                    "peak_hour": "10:00 AM - 11:00 AM",
                    "peak_passengers": 2800,
                    "energy_consumption": {
                        "today_kwh": 12500,
                        "efficiency_score": 8.2
                    }
                }
            }


class MobilePushNotificationService:
    """Service for handling push notifications to mobile devices"""
    
    def __init__(self, mobile_api: MobileAPI):
        self.mobile_api = mobile_api
        self.notification_queue = asyncio.Queue()
        
    async def start(self):
        """Start the notification service"""
        logger.info("Starting mobile push notification service...")
        asyncio.create_task(self.process_notifications())
    
    async def process_notifications(self):
        """Process notification queue"""
        while True:
            try:
                notification = await self.notification_queue.get()
                await self.send_notification(notification)
                self.notification_queue.task_done()
            except Exception as e:
                logger.error(f"Error processing notification: {e}")
                await asyncio.sleep(5)
    
    async def send_notification(self, notification: Dict):
        """Send a push notification to a user"""
        # In a real implementation, this would use a push notification service
        # like Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNS)
        
        logger.info(f"Sending notification to {notification['user_id']}: {notification['title']}")
        
        # Mock: Store notification in user's alert history
        if notification['user_id'] in self.mobile_api.users:
            user = self.mobile_api.users[notification['user_id']]
            if 'notification_history' not in user.preferences:
                user.preferences['notification_history'] = []
            
            user.preferences['notification_history'].append({
                'timestamp': datetime.now().isoformat(),
                'title': notification['title'],
                'message': notification['message'],
                'type': notification['type']
            })
            
            # Keep only recent notifications
            if len(user.preferences['notification_history']) > 50:
                user.preferences['notification_history'] = user.preferences['notification_history'][-50:]
            
            self.mobile_api.save_users()
    
    async def queue_notification(self, user_id: str, title: str, message: str, 
                                notification_type: str = "info", 
                                data: Dict = None):
        """Queue a notification for sending"""
        if user_id not in self.mobile_api.users:
            logger.warning(f"Cannot send notification: user {user_id} not found")
            return False
        
        # Check if user has notifications enabled
        user = self.mobile_api.users[user_id]
        if not user.preferences.get("notifications", True):
            logger.info(f"Notifications disabled for user {user_id}")
            return False
        
        notification = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        await self.notification_queue.put(notification)
        return True
    
    async def broadcast_notification(self, title: str, message: str, 
                                    notification_type: str = "alert",
                                    filter_func = None):
        """Broadcast notification to multiple users"""
        sent_count = 0
        
        for user_id, user in self.mobile_api.users.items():
            # Apply filter if provided
            if filter_func and not filter_func(user):
                continue
            
            if await self.queue_notification(user_id, title, message, notification_type):
                sent_count += 1
        
        logger.info(f"Broadcast notification sent to {sent_count} users")
        return sent_count


async def main():
    """Main entry point for testing"""
    # Initialize mobile API
    mobile_api = MobileAPI()
    
    # Initialize push notification service
    push_service = MobilePushNotificationService(mobile_api)
    await push_service.start()
    
    # Test registration
    logger.info("Testing mobile API...")
    
    # Register a test user
    test_user = mobile_api.register_user("test_device_123", {
        "notifications": True,
        "theme": "dark",
        "favorites": {"stations": ["MK", "Epcot"]}
    })
    
    logger.info(f"Registered test user: {test_user.user_id}")
    logger.info(f"API Key: {test_user.api_key}")
    
    # Test login
    session_token = mobile_api.create_session(test_user)
    logger.info(f"Created session: {session_token}")
    
    # Test push notification
    await push_service.queue_notification(
        test_user.user_id,
        "Welcome to WDW Monorail",
        "Thank you for using our mobile app! Stay informed about monorail status and schedules.",
        "welcome"
    )
    
    # Test broadcast notification
    await push_service.broadcast_notification(
        "System Update",
        "The monorail system is operating normally. Enjoy your day at Walt Disney World!",
        "info"
    )
    
    # Start the FastAPI server
    logger.info("Starting mobile API server on http://0.0.0.0:8003")
    
    config = uvicorn.Config(
        mobile_api.app,
        host="0.0.0.0",
        port=8003,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
