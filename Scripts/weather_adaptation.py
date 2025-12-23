#!/usr/bin/env python3
"""
WDW Monorail Weather Adaptation Module

Adapts monorail operations based on real-time weather conditions.
Adjusts speeds, routing, and safety protocols according to weather data.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)sZ %(levelname)s [WEATHER_ADAPTATION] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("weather_adaptation.log")
    ]
)
logger = logging.getLogger(__name__)


class WeatherData:
    """Represents current weather conditions"""
    
    def __init__(self, temperature: float, humidity: float, 
                 wind_speed: float, wind_direction: float,
                 precipitation: float, visibility: float,
                 conditions: str, timestamp: datetime):
        self.temperature = temperature  # °F
        self.humidity = humidity  # %
        self.wind_speed = wind_speed  # mph
        self.wind_direction = wind_direction  # degrees (0-360)
        self.precipitation = precipitation  # inches/hour
        self.visibility = visibility  # miles
        self.conditions = conditions  # "clear", "rain", "thunderstorm", etc.
        self.timestamp = timestamp
        
    def is_severe_weather(self) -> bool:
        """Check if current conditions constitute severe weather"""
        return (
            self.wind_speed > 30 or  # High winds
            self.precipitation > 0.5 or  # Heavy rain
            "thunderstorm" in self.conditions.lower() or
            "tornado" in self.conditions.lower() or
            "hurricane" in self.conditions.lower()
        )
    
    def get_weather_severity(self) -> str:
        """Get weather severity level"""
        if self.is_severe_weather():
            return "severe"
        elif (
            self.wind_speed > 20 or
            self.precipitation > 0.2 or
            "rain" in self.conditions.lower()
        ):
            return "moderate"
        else:
            return "normal"
    
    def to_dict(self) -> Dict:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "precipitation": self.precipitation,
            "visibility": self.visibility,
            "conditions": self.conditions,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.get_weather_severity()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            temperature=data["temperature"],
            humidity=data["humidity"],
            wind_speed=data["wind_speed"],
            wind_direction=data["wind_direction"],
            precipitation=data["precipitation"],
            visibility=data["visibility"],
            conditions=data["conditions"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


class WeatherAdapter:
    """Adapts monorail operations based on weather conditions"""
    
    def __init__(self):
        self.current_weather: Optional[WeatherData] = None
        self.weather_history: List[WeatherData] = []
        self.api_key = os.getenv("WEATHER_API_KEY", "default_key")
        self.location = "Orlando,FL"  # Walt Disney World location
        self.load_weather_data()
        
    def load_weather_data(self):
        """Load weather data from file"""
        try:
            if os.path.exists("weather_data.json"):
                with open("weather_data.json", "r") as f:
                    data = json.load(f)
                    self.weather_history = [WeatherData.from_dict(item) for item in data]
                    if self.weather_history:
                        self.current_weather = self.weather_history[-1]
                logger.info(f"Loaded {len(self.weather_history)} weather records")
        except Exception as e:
            logger.error(f"Error loading weather data: {e}")
    
    def save_weather_data(self):
        """Save weather data to file"""
        try:
            with open("weather_data.json", "w") as f:
                json.dump([w.to_dict() for w in self.weather_history], f, indent=2)
            logger.info(f"Saved {len(self.weather_history)} weather records")
        except Exception as e:
            logger.error(f"Error saving weather data: {e}")
    
    async def fetch_current_weather(self) -> Optional[WeatherData]:
        """Fetch current weather from API"""
        # In a real implementation, this would call a weather API
        # For this example, we'll use mock data
        
        # Mock data - simulate different weather conditions
        import random
        conditions = ["clear", "partly cloudy", "rain", "thunderstorm", "windy"]
        
        mock_weather = WeatherData(
            temperature=75 + random.uniform(-10, 10),
            humidity=60 + random.uniform(-20, 20),
            wind_speed=random.uniform(5, 25),
            wind_direction=random.uniform(0, 360),
            precipitation=random.uniform(0, 0.8),
            visibility=10 - random.uniform(0, 5),
            conditions=random.choice(conditions),
            timestamp=datetime.now()
        )
        
        self.current_weather = mock_weather
        self.weather_history.append(mock_weather)
        
        # Keep only recent history
        if len(self.weather_history) > 100:
            self.weather_history = self.weather_history[-100:]
        
        self.save_weather_data()
        return mock_weather
    
    def get_speed_adjustment_factor(self) -> float:
        """Get speed adjustment factor based on current weather"""
        if not self.current_weather:
            return 1.0  # No adjustment
        
        severity = self.current_weather.get_weather_severity()
        
        if severity == "severe":
            return 0.6  # 40% speed reduction
        elif severity == "moderate":
            return 0.8  # 20% speed reduction
        else:
            return 1.0  # No adjustment
    
    def get_safety_recommendations(self) -> Dict:
        """Get safety recommendations based on current weather"""
        if not self.current_weather:
            return {"recommendations": ["No weather data available"], "severity": "unknown"}
        
        severity = self.current_weather.get_weather_severity()
        recommendations = []
        
        if severity == "severe":
            recommendations.extend([
                "Reduce all monorail speeds by 40%",
                "Increase braking distance by 50%",
                "Suspend outdoor maintenance operations",
                "Activate emergency weather protocols",
                "Increase station staffing for passenger assistance",
                "Prepare for potential service disruptions"
            ])
        elif severity == "moderate":
            recommendations.extend([
                "Reduce monorail speeds by 20%",
                "Increase braking distance by 30%",
                "Monitor weather conditions closely",
                "Be prepared for sudden weather changes",
                "Increase maintenance checks on outdoor equipment"
            ])
        else:
            recommendations.append("Normal operations - monitor weather conditions")
        
        return {
            "recommendations": recommendations,
            "severity": severity,
            "current_conditions": self.current_weather.conditions,
            "wind_speed": self.current_weather.wind_speed,
            "precipitation": self.current_weather.precipitation,
            "visibility": self.current_weather.visibility
        }
    
    def get_route_adjustments(self) -> Dict:
        """Get recommended route adjustments based on weather"""
        if not self.current_weather:
            return {"adjustments": [], "severity": "unknown"}
        
        severity = self.current_weather.get_weather_severity()
        adjustments = []
        
        if severity == "severe":
            adjustments.extend([
                {
                    "route": "all",
                    "adjustment": "Suspend service",
                    "reason": "Severe weather conditions"
                }
            ])
        elif severity == "moderate" and self.current_weather.wind_speed > 25:
            adjustments.extend([
                {
                    "route": "express",
                    "adjustment": "Temporary suspension",
                    "reason": "High crosswinds on elevated sections"
                },
                {
                    "route": "resort",
                    "adjustment": "Reduced frequency",
                    "reason": "Safety precautions for ground-level sections"
                }
            ])
        elif severity == "moderate" and self.current_weather.precipitation > 0.3:
            adjustments.extend([
                {
                    "route": "all",
                    "adjustment": "Reduced speed in curves",
                    "reason": "Wet track conditions"
                }
            ])
        
        return {
            "adjustments": adjustments,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_weather_impact_analysis(self) -> Dict:
        """Analyze the impact of current weather on operations"""
        if not self.current_weather:
            return {"error": "No weather data available"}
        
        severity = self.current_weather.get_weather_severity()
        
        # Impact analysis
        if severity == "severe":
            impact = {
                "operational_impact": "Significant disruptions expected",
                "safety_risk": "High",
                "passenger_impact": "Major delays or service suspensions",
                "maintenance_impact": "Outdoor maintenance halted",
                "estimated_capacity_reduction": "50-70%"
            }
        elif severity == "moderate":
            impact = {
                "operational_impact": "Minor to moderate delays",
                "safety_risk": "Moderate",
                "passenger_impact": "Increased travel times (15-30% longer)",
                "maintenance_impact": "Increased inspection frequency",
                "estimated_capacity_reduction": "10-30%"
            }
        else:
            impact = {
                "operational_impact": "Normal operations",
                "safety_risk": "Low",
                "passenger_impact": "None",
                "maintenance_impact": "Normal schedule",
                "estimated_capacity_reduction": "0%"
            }
        
        return {
            "current_weather": self.current_weather.to_dict(),
            "impact_analysis": impact,
            "recommendations": self.get_safety_recommendations()["recommendations"]
        }


class WeatherAdaptationSystem:
    """Main weather adaptation system"""
    
    def __init__(self):
        self.weather_adapter = WeatherAdapter()
        self.weather_alerts = []
        
    async def initialize(self):
        """Initialize the weather adaptation system"""
        # Fetch current weather
        await self.weather_adapter.fetch_current_weather()
        
        # Start weather monitoring
        asyncio.create_task(self.monitor_weather_conditions())
        
        logger.info("Weather adaptation system initialized")
    
    async def monitor_weather_conditions(self):
        """Continuously monitor weather conditions"""
        logger.info("Starting weather condition monitoring...")
        
        while True:
            try:
                # Fetch updated weather
                weather = await self.weather_adapter.fetch_current_weather()
                
                if weather:
                    severity = weather.get_weather_severity()
                    logger.info(f"Current weather: {weather.conditions}, Severity: {severity}")
                    
                    # Check for severe weather alerts
                    if severity == "severe":
                        alert = {
                            "timestamp": datetime.now().isoformat(),
                            "severity": severity,
                            "conditions": weather.conditions,
                            "message": f"SEVERE WEATHER ALERT: {weather.conditions} with {weather.wind_speed} mph winds and {weather.precipitation} in/hr precipitation"
                        }
                        self.weather_alerts.append(alert)
                        logger.warning(f"WEATHER ALERT: {alert['message']}")
                    
                    # Get and log recommendations
                    recommendations = self.weather_adapter.get_safety_recommendations()
                    if recommendations["severity"] != "normal":
                        logger.info(f"Weather recommendations: {recommendations['recommendations']}")
                
                await asyncio.sleep(900)  # Check every 15 minutes
                
            except Exception as e:
                logger.error(f"Error in weather monitoring: {e}")
                await asyncio.sleep(300)
    
    def get_current_weather_adaptation(self) -> Dict:
        """Get current weather adaptation status"""
        if not self.weather_adapter.current_weather:
            return {"status": "no_data", "message": "Weather data not available"}
        
        return {
            "current_weather": self.weather_adapter.current_weather.to_dict(),
            "speed_adjustment_factor": self.weather_adapter.get_speed_adjustment_factor(),
            "safety_recommendations": self.weather_adapter.get_safety_recommendations(),
            "route_adjustments": self.weather_adapter.get_route_adjustments(),
            "weather_alerts": self.weather_alerts[-5:],  # Last 5 alerts
            "last_updated": datetime.now().isoformat()
        }
    
    def get_weather_forecast_impact(self, hours_ahead: int = 6) -> Dict:
        """Predict impact of forecasted weather (mock implementation)"""
        # In a real system, this would use actual weather forecast data
        
        # Mock forecast - assume weather will be similar to current
        current = self.weather_adapter.current_weather
        if not current:
            return {"error": "No current weather data available"}
        
        # Simple forecast: assume current conditions persist
        forecast_conditions = current.conditions
        
        # Add some variation
        import random
        if "rain" in forecast_conditions.lower():
            # Rain might intensify or weaken
            if random.random() > 0.7:
                forecast_conditions = "heavy rain" if "heavy" not in forecast_conditions else "light rain"
        
        # Predict impact
        if "severe" in current.get_weather_severity():
            impact = "continued severe impact"
        elif "moderate" in current.get_weather_severity():
            impact = "continued moderate impact"
        else:
            impact = "no significant impact expected"
        
        return {
            "forecast_period_hours": hours_ahead,
            "predicted_conditions": forecast_conditions,
            "predicted_impact": impact,
            "recommended_preparations": self.weather_adapter.get_safety_recommendations()["recommendations"],
            "confidence": "low"  # Mock data has low confidence
        }
    
    async def get_real_weather_data(self) -> Optional[WeatherData]:
        """Fetch real weather data from API (implementation example)"""
        # This would be the real implementation using a weather API
        
        WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"
        
        params = {
            "key": self.weather_adapter.api_key,
            "q": self.weather_adapter.location
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(WEATHER_API_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Parse weather data
                        current = data.get("current", {})
                        condition = current.get("condition", {}).get("text", "unknown")
                        
                        weather = WeatherData(
                            temperature=current.get("temp_f", 75.0),
                            humidity=current.get("humidity", 65),
                            wind_speed=current.get("wind_mph", 10.0),
                            wind_direction=current.get("wind_degree", 180),
                            precipitation=current.get("precip_in", 0.0),
                            visibility=current.get("vis_miles", 10.0),
                            conditions=condition,
                            timestamp=datetime.now()
                        )
                        
                        return weather
                    else:
                        logger.error(f"Weather API error: {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"Error fetching real weather data: {e}")
            return None


async def main():
    """Main entry point for testing"""
    # Initialize system
    was = WeatherAdaptationSystem()
    await was.initialize()
    
    # Test weather adaptation
    logger.info("Weather Adaptation System Status:")
    
    # Get current adaptation status
    status = was.get_current_weather_adaptation()
    logger.info(f"Current weather: {status['current_weather']['conditions']}")
    logger.info(f"Severity: {status['current_weather']['severity']}")
    logger.info(f"Speed adjustment factor: {status['speed_adjustment_factor']}")
    
    # Get safety recommendations
    recommendations = status['safety_recommendations']
    logger.info(f"Safety recommendations ({recommendations['severity']}):")
    for rec in recommendations['recommendations']:
        logger.info(f"  - {rec}")
    
    # Get route adjustments
    route_adjustments = status['route_adjustments']
    logger.info(f"Route adjustments:")
    if route_adjustments['adjustments']:
        for adj in route_adjustments['adjustments']:
            logger.info(f"  - {adj['route']}: {adj['adjustment']} ({adj['reason']})")
    else:
        logger.info(f"  - No route adjustments needed")
    
    # Get weather impact analysis
    impact = was.weather_adapter.get_weather_impact_analysis()
    logger.info(f"Weather impact analysis:")
    for key, value in impact['impact_analysis'].items():
        logger.info(f"  - {key}: {value}")
    
    # Test weather forecast impact
    forecast = was.get_weather_forecast_impact(hours_ahead=6)
    logger.info(f"Weather forecast (next 6 hours):")
    logger.info(f"  - Predicted conditions: {forecast['predicted_conditions']}")
    logger.info(f"  - Predicted impact: {forecast['predicted_impact']}")
    
    # Simulate weather change
    logger.info("\nSimulating weather change to severe conditions...")
    
    # Create severe weather condition
    severe_weather = WeatherData(
        temperature=72.0,
        humidity=85.0,
        wind_speed=35.0,
        wind_direction=180.0,
        precipitation=0.8,
        visibility=2.0,
        conditions="severe thunderstorm",
        timestamp=datetime.now()
    )
    
    was.weather_adapter.current_weather = severe_weather
    was.weather_adapter.weather_history.append(severe_weather)
    
    # Get updated recommendations
    updated_status = was.get_current_weather_adaptation()
    logger.info(f"Updated weather: {updated_status['current_weather']['conditions']}")
    logger.info(f"New severity: {updated_status['current_weather']['severity']}")
    logger.info(f"New speed adjustment factor: {updated_status['speed_adjustment_factor']}")
    
    updated_recommendations = updated_status['safety_recommendations']
    logger.info(f"Updated safety recommendations:")
    for rec in updated_recommendations['recommendations']:
        logger.info(f"  - {rec}")


if __name__ == "__main__":
    asyncio.run(main())
