#!/usr/bin/env python3
"""
Engine Lights Control for WDW Monorail System

This script simulates blinking engine lights for the monorail fleet.
It can be integrated with the main automation system for hardware control.
"""

import time
import threading
from typing import Dict, Optional


class EngineLightsController:
    """Control engine lights for the monorail fleet."""

    def __init__(self):
        self.lights_state: Dict[str, bool] = {
            "Red": False,
            "Orange": False,
            "Yellow": False,
            "Green": False,
            "Blue": False,
            "Coral": False,
            "Lime": False,
            "Teal": False,
            "Gold": False,
            "Peach": False,
            "Silver": False,
            "Black": False,
        }
        self.threads: Dict[str, Optional[threading.Thread]] = {color: None for color in self.lights_state}
        self.stop_events: Dict[str, threading.Event] = {color: threading.Event() for color in self.lights_state}

    def blink_lights(self, train_color: str, interval: float = 1.0) -> None:
        """Blink lights for a specific monorail."""
        if train_color not in self.lights_state:
            print(f"Error: Unknown train color '{train_color}'")
            return

        # Stop any existing blinking thread for this train
        if self.threads[train_color] and self.threads[train_color].is_alive():
            self.stop_events[train_color].set()
            self.threads[train_color].join()

        # Reset stop event
        self.stop_events[train_color].clear()

        def blink():
            while not self.stop_events[train_color].is_set():
                self.lights_state[train_color] = not self.lights_state[train_color]
                status = "ON" if self.lights_state[train_color] else "OFF"
                print(f"{train_color} engine lights: {status}")
                time.sleep(interval)

        self.threads[train_color] = threading.Thread(target=blink, daemon=True)
        self.threads[train_color].start()

    def stop_blinking(self, train_color: str) -> None:
        """Stop blinking lights for a specific monorail."""
        if train_color in self.stop_events:
            self.stop_events[train_color].set()
            if self.threads[train_color]:
                self.threads[train_color].join()
            self.lights_state[train_color] = False

    def stop_all(self) -> None:
        """Stop all blinking lights."""
        for color in self.lights_state:
            self.stop_blinking(color)

    def get_status(self, train_color: str) -> str:
        """Get the current status of a monorail's lights."""
        if train_color not in self.lights_state:
            return f"Error: Unknown train color '{train_color}'"
        return "ON" if self.lights_state[train_color] else "OFF"

    def sos_blink(self, train_color: str) -> None:
        """Blink lights in SOS pattern (3 short, 3 long, 3 short)."""
        if train_color not in self.lights_state:
            print(f"Error: Unknown train color '{train_color}'")
            return

        # Stop any existing blinking thread for this train
        if self.threads[train_color] and self.threads[train_color].is_alive():
            self.stop_events[train_color].set()
            self.threads[train_color].join()

        # Reset stop event
        self.stop_events[train_color].clear()

        def sos():
            pattern = [0.2, 0.2, 0.2, 0.6, 0.6, 0.6, 0.2, 0.2, 0.2]  # 3 short, 3 long, 3 short
            while not self.stop_events[train_color].is_set():
                for duration in pattern:
                    if self.stop_events[train_color].is_set():
                        break
                    self.lights_state[train_color] = True
                    print(f"{train_color} engine lights: SOS ON")
                    time.sleep(duration)
                    self.lights_state[train_color] = False
                    print(f"{train_color} engine lights: SOS OFF")
                    time.sleep(0.2)  # Gap between signals
                time.sleep(1.0)  # Gap between SOS sequences

        self.threads[train_color] = threading.Thread(target=sos, daemon=True)
        self.threads[train_color].start()

    def emergency_stop(self, train_color: str) -> None:
        """Simulate emergency stop with SOS blinking."""
        print(f"EMERGENCY STOP: {train_color} monorail")
        self.sos_blink(train_color)

    def emergency_stop_all(self) -> None:
        """Simulate emergency stop for all monorails."""
        print("EMERGENCY STOP: ALL monorails")
        for color in self.lights_state:
            self.sos_blink(color)

    def validate_train_color(self, train_color: str) -> bool:
        """Validate that the train color exists in the fleet."""
        return train_color in self.lights_state

    def check_system_health(self) -> Dict[str, str]:
        """Check the health status of all monorail light systems."""
        health_status = {}
        for color in self.lights_state:
            thread_status = "Active" if self.threads[color] and self.threads[color].is_alive() else "Inactive"
            health_status[color] = f"Lights: {'ON' if self.lights_state[color] else 'OFF'}, Thread: {thread_status}"
        return health_status

    def handle_error(self, train_color: str, error_type: str) -> None:
        """Handle errors by triggering appropriate responses."""
        print(f"ERROR DETECTED: {error_type} on {train_color} monorail")
        
        if error_type == "motor_failure":
            # Critical failure - emergency stop with SOS
            self.emergency_stop(train_color)
        elif error_type == "sensor_failure":
            # Non-critical but serious - SOS pattern
            self.sos_blink(train_color)
        elif error_type == "communication_error":
            # Blink rapidly to indicate communication issues
            self.blink_lights(train_color, 0.3)
        else:
            # Unknown error - SOS pattern
            self.sos_blink(train_color)


if __name__ == "__main__":
    controller = EngineLightsController()

    print("WDW Monorail Engine Lights Control")
    print("Type 'help' for commands, 'exit' to quit")

    while True:
        try:
            cmd = input("> ").strip().lower()

            if cmd == "exit":
                controller.stop_all()
                break

            elif cmd == "help":
                print("\nAvailable commands:")
                print("  blink <color> [interval] - Start blinking lights (default interval: 1.0s)")
                print("  sos <color> - Start SOS blinking pattern for a specific monorail")
                print("  emergency <color> - Simulate emergency stop with SOS for a specific monorail")
                print("  emergency all - Simulate emergency stop with SOS for all monorails")
                print("  error <color> <type> - Simulate error handling (types: motor_failure, sensor_failure, communication_error)")
                print("  health - Check system health status for all monorails")
                print("  stop <color> - Stop blinking lights for a specific monorail")
                print("  stop all - Stop all blinking lights")
                print("  status <color> - Get current status of a monorail's lights")
                print("  list - List all monorail colors")
                print("  help - Show this help message")
                print("  exit - Exit the program")

            elif cmd.startswith("blink"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Error: Please specify a train color")
                    continue

                color = parts[1].capitalize()
                interval = float(parts[2]) if len(parts) >= 3 else 1.0

                if color in controller.lights_state:
                    controller.blink_lights(color, interval)
                    print(f"Started blinking {color} lights at {interval}s interval")
                else:
                    print(f"Error: Unknown train color '{color}'")

            elif cmd.startswith("stop"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Error: Please specify 'all' or a train color")
                    continue

                if parts[1].lower() == "all":
                    controller.stop_all()
                    print("Stopped all blinking lights")
                else:
                    color = parts[1].capitalize()
                    if color in controller.lights_state:
                        controller.stop_blinking(color)
                        print(f"Stopped blinking {color} lights")
                    else:
                        print(f"Error: Unknown train color '{color}'")

            elif cmd.startswith("status"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Error: Please specify a train color")
                    continue

                color = parts[1].capitalize()
                if color in controller.lights_state:
                    status = controller.get_status(color)
                    print(f"{color} lights status: {status}")
                else:
                    print(f"Error: Unknown train color '{color}'")

            elif cmd == "list":
                print("Available monorail colors:")
                for color in controller.lights_state:
                    print(f"  - {color}")

            elif cmd.startswith("sos"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Error: Please specify a train color")
                    continue

                color = parts[1].capitalize()
                if color in controller.lights_state:
                    controller.sos_blink(color)
                    print(f"Started SOS blinking for {color} monorail")
                else:
                    print(f"Error: Unknown train color '{color}'")

            elif cmd.startswith("emergency"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Error: Please specify 'all' or a train color")
                    continue

                if parts[1].lower() == "all":
                    controller.emergency_stop_all()
                else:
                    color = parts[1].capitalize()
                    if color in controller.lights_state:
                        controller.emergency_stop(color)
                    else:
                        print(f"Error: Unknown train color '{color}'")

            elif cmd == "health":
                health_status = controller.check_system_health()
                print("\nSystem Health Status:")
                for color, status in health_status.items():
                    print(f"  {color}: {status}")

            elif cmd.startswith("error"):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Error: Please specify a train color and error type")
                    print("Usage: error <color> <error_type>")
                    print("Error types: motor_failure, sensor_failure, communication_error")
                    continue

                color = parts[1].capitalize()
                error_type = parts[2]
                
                if color in controller.lights_state:
                    controller.handle_error(color, error_type)
                    print(f"Handling {error_type} error for {color} monorail")
                else:
                    print(f"Error: Unknown train color '{color}'")

            else:
                print("Error: Unknown command. Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nStopping all lights...")
            controller.stop_all()
            break
        except Exception as e:
            print(f"Error: {e}")







