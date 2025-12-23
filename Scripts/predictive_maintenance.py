#!/usr/bin/env python3
"""
WDW Monorail Predictive Maintenance System

Machine learning-based predictive maintenance for monorail fleet.
Analyzes sensor data, usage patterns, and historical maintenance records
to predict when maintenance will be required.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.preprocessing import StandardScaler
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)sZ %(levelname)s [PREDICTIVE_MAINTENANCE] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("predictive_maintenance.log")
    ]
)
logger = logging.getLogger(__name__)


class MaintenanceRecord:
    """Represents a single maintenance event"""
    
    def __init__(self, monorail_id: str, maintenance_type: str, 
                 date: datetime, component: str, severity: int, 
                 description: str, parts_replaced: List[str] = None):
        self.monorail_id = monorail_id
        self.maintenance_type = maintenance_type  # "preventive", "corrective", "emergency"
        self.date = date
        self.component = component  # "motor", "brakes", "sensors", "wheels", "electrical"
        self.severity = severity  # 1-5 scale
        self.description = description
        self.parts_replaced = parts_replaced or []
        
    def to_dict(self) -> Dict:
        return {
            "monorail_id": self.monorail_id,
            "maintenance_type": self.maintenance_type,
            "date": self.date.isoformat(),
            "component": self.component,
            "severity": self.severity,
            "description": self.description,
            "parts_replaced": self.parts_replaced
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            monorail_id=data["monorail_id"],
            maintenance_type=data["maintenance_type"],
            date=datetime.fromisoformat(data["date"]),
            component=data["component"],
            severity=data["severity"],
            description=data["description"],
            parts_replaced=data.get("parts_replaced", [])
        )


class MonorailHealthMonitor:
    """Monitors real-time health metrics for a monorail"""
    
    def __init__(self, monorail_id: str):
        self.monorail_id = monorail_id
        self.metrics: Dict[str, List[Tuple[datetime, float]]] = {
            "motor_temperature": [],
            "bearing_vibration": [],
            "braking_distance": [],
            "power_consumption": [],
            "speed_fluctuations": [],
            "sensor_errors": []
        }
        self.alert_thresholds = {
            "motor_temperature": 85.0,  # °C
            "bearing_vibration": 2.5,   # mm/s
            "braking_distance": 220.0,  # ft
            "power_consumption": 1500.0, # W
            "speed_fluctuations": 1.5,  # mph
            "sensor_errors": 3.0         # errors/hour
        }
    
    def add_metric(self, metric_name: str, value: float):
        """Add a new metric reading"""
        if metric_name in self.metrics:
            self.metrics[metric_name].append((datetime.now(), value))
            # Keep only last 1000 readings
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-1000:]
            
            # Check for alerts
            if value > self.alert_thresholds.get(metric_name, float('inf')):
                logger.warning(f"ALERT: {self.monorail_id} {metric_name}={value:.2f} exceeds threshold")
                return True
        return False
    
    def get_recent_metrics(self, hours: int = 24) -> Dict[str, List[float]]:
        """Get metrics from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = {}
        for metric, values in self.metrics.items():
            recent[metric] = [v for t, v in values if t >= cutoff]
        return recent
    
    def calculate_health_score(self) -> float:
        """Calculate overall health score (0-100)"""
        recent = self.get_recent_metrics(hours=24)
        
        # Simple scoring algorithm
        score = 100.0
        for metric, values in recent.items():
            if values:
                avg = sum(values) / len(values)
                threshold = self.alert_thresholds[metric]
                # Penalize based on proximity to threshold
                if avg > threshold * 0.8:
                    penalty = 20 * ((avg - threshold * 0.8) / (threshold * 0.2))
                    score = max(0, score - penalty)
        
        return round(score, 1)


class PredictiveMaintenanceSystem:
    """Main predictive maintenance system"""
    
    def __init__(self):
        self.maintenance_records: Dict[str, List[MaintenanceRecord]] = {}
        self.health_monitors: Dict[str, MonorailHealthMonitor] = {}
        self.model = None
        self.scaler = None
        self.trained = False
        self.load_data()
        
    def load_data(self):
        """Load maintenance records from file"""
        try:
            if os.path.exists("maintenance_data.json"):
                with open("maintenance_data.json", "r") as f:
                    data = json.load(f)
                    for record_data in data:
                        record = MaintenanceRecord.from_dict(record_data)
                        if record.monorail_id not in self.maintenance_records:
                            self.maintenance_records[record.monorail_id] = []
                        self.maintenance_records[record.monorail_id].append(record)
                logger.info(f"Loaded {len(data)} maintenance records")
        except Exception as e:
            logger.error(f"Error loading maintenance data: {e}")
    
    def save_data(self):
        """Save maintenance records to file"""
        try:
            records = []
            for monorail_records in self.maintenance_records.values():
                records.extend([r.to_dict() for r in monorail_records])
            
            with open("maintenance_data.json", "w") as f:
                json.dump(records, f, indent=2)
            logger.info(f"Saved {len(records)} maintenance records")
        except Exception as e:
            logger.error(f"Error saving maintenance data: {e}")
    
    def add_maintenance_record(self, record: MaintenanceRecord):
        """Add a new maintenance record"""
        if record.monorail_id not in self.maintenance_records:
            self.maintenance_records[record.monorail_id] = []
        self.maintenance_records[record.monorail_id].append(record)
        self.save_data()
    
    def get_maintenance_history(self, monorail_id: str) -> List[MaintenanceRecord]:
        """Get maintenance history for a specific monorail"""
        return self.maintenance_records.get(monorail_id, [])
    
    def add_health_monitor(self, monorail_id: str) -> MonorailHealthMonitor:
        """Add or get health monitor for a monorail"""
        if monorail_id not in self.health_monitors:
            self.health_monitors[monorail_id] = MonorailHealthMonitor(monorail_id)
        return self.health_monitors[monorail_id]
    
    def get_health_monitor(self, monorail_id: str) -> Optional[MonorailHealthMonitor]:
        """Get health monitor for a monorail"""
        return self.health_monitors.get(monorail_id)
    
    def train_model(self):
        """Train the predictive maintenance model"""
        if not self.maintenance_records:
            logger.warning("No maintenance data available for training")
            return
        
        # Prepare training data
        X, y = self._prepare_training_data()
        
        if len(X) < 10:  # Minimum samples for training
            logger.warning(f"Insufficient training data: {len(X)} samples")
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        
        logger.info(f"Model trained - Accuracy: {accuracy:.3f}, Precision: {precision:.3f}")
        self.trained = True
        
        # Save model
        joblib.dump(self.model, "predictive_maintenance_model.pkl")
        joblib.dump(self.scaler, "predictive_maintenance_scaler.pkl")
    
    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from maintenance records"""
        features = []
        labels = []  # 0 = no maintenance needed, 1 = maintenance needed
        
        for monorail_id, records in self.maintenance_records.items():
            # Sort records by date
            records.sort(key=lambda r: r.date)
            
            for i, record in enumerate(records):
                # Get metrics before this maintenance event
                monitor = self.get_health_monitor(monorail_id)
                if not monitor:
                    continue
                
                # Get metrics from 24 hours before maintenance
                before_maintenance = record.date - timedelta(hours=24)
                recent_metrics = {}
                
                for timestamp, value in monitor.metrics.get("motor_temperature", []):
                    if before_maintenance <= timestamp <= record.date:
                        if "motor_temperature" not in recent_metrics:
                            recent_metrics["motor_temperature"] = []
                        recent_metrics["motor_temperature"].append(value)
                
                # Calculate average metrics
                feature_vector = []
                
                # Add metric averages
                for metric in ["motor_temperature", "bearing_vibration", "braking_distance",
                             "power_consumption", "speed_fluctuations", "sensor_errors"]:
                    if metric in recent_metrics and recent_metrics[metric]:
                        avg = sum(recent_metrics[metric]) / len(recent_metrics[metric])
                        feature_vector.append(avg)
                    else:
                        feature_vector.append(0)
                
                # Add time since last maintenance
                if i > 0:
                    days_since = (record.date - records[i-1].date).days
                    feature_vector.append(days_since)
                else:
                    feature_vector.append(30)  # Default if no previous maintenance
                
                # Add component-specific features
                component_features = {
                    "motor": [1, 0, 0, 0],
                    "brakes": [0, 1, 0, 0],
                    "sensors": [0, 0, 1, 0],
                    "wheels": [0, 0, 0, 1],
                    "electrical": [0, 0, 0, 0]
                }.get(record.component, [0, 0, 0, 0])
                feature_vector.extend(component_features)
                
                # Label: 1 if this was emergency/corrective maintenance, 0 if preventive
                label = 1 if record.maintenance_type in ["corrective", "emergency"] else 0
                
                features.append(feature_vector)
                labels.append(label)
        
        return np.array(features), np.array(labels)
    
    def predict_maintenance(self, monorail_id: str) -> Dict:
        """Predict maintenance needs for a monorail"""
        if not self.trained or not self.model:
            logger.warning("Model not trained - using heuristic approach")
            return self._heuristic_prediction(monorail_id)
        
        monitor = self.get_health_monitor(monorail_id)
        if not monitor:
            return {"prediction": "unknown", "confidence": 0, "recommendation": "No data available"}
        
        # Prepare feature vector
        feature_vector = []
        recent_metrics = monitor.get_recent_metrics(hours=24)
        
        # Add metric averages
        for metric in ["motor_temperature", "bearing_vibration", "braking_distance",
                     "power_consumption", "speed_fluctuations", "sensor_errors"]:
            if recent_metrics.get(metric):
                avg = sum(recent_metrics[metric]) / len(recent_metrics[metric])
                feature_vector.append(avg)
            else:
                feature_vector.append(0)
        
        # Add time since last maintenance
        last_maintenance = self.get_maintenance_history(monorail_id)
        if last_maintenance:
            days_since = (datetime.now() - last_maintenance[-1].date).days
            feature_vector.append(days_since)
        else:
            feature_vector.append(30)
        
        # Add default component features (will be updated based on current issues)
        feature_vector.extend([0, 0, 0, 0])
        
        # Scale features
        if self.scaler:
            feature_vector_scaled = self.scaler.transform([feature_vector])
        else:
            feature_vector_scaled = [feature_vector]
        
        # Predict
        prediction = self.model.predict(feature_vector_scaled)[0]
        probabilities = self.model.predict_proba(feature_vector_scaled)[0]
        confidence = max(probabilities)
        
        # Generate recommendation
        if prediction == 1:
            # Maintenance needed
            health_score = monitor.calculate_health_score()
            if health_score < 30:
                recommendation = "IMMEDIATE MAINTENANCE REQUIRED"
            elif health_score < 60:
                recommendation = "Schedule maintenance within 24 hours"
            else:
                recommendation = "Monitor closely, schedule maintenance soon"
        else:
            # No maintenance needed
            health_score = monitor.calculate_health_score()
            if health_score > 80:
                recommendation = "System operating normally"
            else:
                recommendation = "System operating normally, routine maintenance recommended"
        
        return {
            "prediction": "maintenance_needed" if prediction == 1 else "no_maintenance",
            "confidence": float(confidence),
            "health_score": health_score,
            "recommendation": recommendation,
            "last_maintenance": last_maintenance[-1].date.isoformat() if last_maintenance else None,
            "metrics": {k: (sum(v)/len(v) if v else 0) for k, v in recent_metrics.items()}
        }
    
    def _heuristic_prediction(self, monorail_id: str) -> Dict:
        """Heuristic prediction when model is not trained"""
        monitor = self.get_health_monitor(monorail_id)
        if not monitor:
            return {"prediction": "unknown", "confidence": 0, "recommendation": "No data available"}
        
        health_score = monitor.calculate_health_score()
        recent_metrics = monitor.get_recent_metrics(hours=24)
        
        # Check for any metrics exceeding thresholds
        critical_issues = []
        for metric, values in recent_metrics.items():
            if values and max(values) > monitor.alert_thresholds[metric]:
                critical_issues.append(metric)
        
        if critical_issues:
            return {
                "prediction": "maintenance_needed",
                "confidence": 0.9,
                "health_score": health_score,
                "recommendation": f"IMMEDIATE MAINTENANCE: {', '.join(critical_issues)} exceed thresholds",
                "critical_issues": critical_issues
            }
        elif health_score < 50:
            return {
                "prediction": "maintenance_needed",
                "confidence": 0.7,
                "health_score": health_score,
                "recommendation": "Schedule maintenance soon - health score low"
            }
        else:
            return {
                "prediction": "no_maintenance",
                "confidence": 0.8,
                "health_score": health_score,
                "recommendation": "System operating normally"
            }
    
    async def monitor_fleet_health(self):
        """Continuously monitor fleet health"""
        logger.info("Starting fleet health monitoring...")
        
        while True:
            try:
                for monorail_id, monitor in self.health_monitors.items():
                    health_score = monitor.calculate_health_score()
                    prediction = self.predict_maintenance(monorail_id)
                    
                    if prediction["prediction"] == "maintenance_needed":
                        logger.warning(f"{monorail_id}: {prediction['recommendation']} (Score: {health_score})")
                    elif health_score < 70:
                        logger.info(f"{monorail_id}: Health score {health_score} - monitoring")
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in fleet health monitoring: {e}")
                await asyncio.sleep(60)


async def main():
    """Main entry point for testing"""
    # Initialize system
    pms = PredictiveMaintenanceSystem()
    
    # Add some sample data if none exists
    if not pms.maintenance_records:
        logger.info("Adding sample maintenance data...")
        
        # Add sample maintenance records
        now = datetime.now()
        sample_records = [
            MaintenanceRecord(
                monorail_id="monorail_red",
                maintenance_type="preventive",
                date=now - timedelta(days=30),
                component="motor",
                severity=2,
                description="Routine motor inspection and lubrication"
            ),
            MaintenanceRecord(
                monorail_id="monorail_red",
                maintenance_type="corrective",
                date=now - timedelta(days=15),
                component="brakes",
                severity=3,
                description="Brake pad replacement due to wear"
            ),
            MaintenanceRecord(
                monorail_id="monorail_blue",
                maintenance_type="emergency",
                date=now - timedelta(days=7),
                component="sensors",
                severity=4,
                description="Emergency sensor replacement after failure"
            )
        ]
        
        for record in sample_records:
            pms.add_maintenance_record(record)
    
    # Add health monitors for sample monorails
    for monorail_id in ["monorail_red", "monorail_blue", "monorail_green"]:
        monitor = pms.add_health_monitor(monorail_id)
        
        # Add some sample metrics
        monitor.add_metric("motor_temperature", 75.0)
        monitor.add_metric("bearing_vibration", 1.2)
        monitor.add_metric("braking_distance", 210.0)
        monitor.add_metric("power_consumption", 1200.0)
    
    # Train the model
    pms.train_model()
    
    # Test predictions
    for monorail_id in ["monorail_red", "monorail_blue", "monorail_green"]:
        prediction = pms.predict_maintenance(monorail_id)
        logger.info(f"{monorail_id} prediction: {prediction}")
    
    # Start monitoring (in a real system, this would run continuously)
    # await pms.monitor_fleet_health()


if __name__ == "__main__":
    asyncio.run(main())
