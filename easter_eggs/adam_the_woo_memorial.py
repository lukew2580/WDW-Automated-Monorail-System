#!/usr/bin/env python3

"""
Adam the Woo Memorial Easter Egg
This script is a tribute to Adam the Woo, a beloved figure in the Disney community.
"""

import random
import time
import json

def load_voice_database():
    """
    Load the vocal tones and characteristics from the JSON database.
    """
    with open('/home/workspace/WDW-Automated-Monorail-System/easter_eggs/adam_the_woo_voice_database.json', 'r') as file:
        return json.load(file)

def simulate_vocal_tone(tone_description, message):
    """
    Simulate the vocal tone by adding emphasis or styling to the message.
    """
    if "enthusiastic" in tone_description:
        return f"🎢 {message.upper()}! 🎢"
    elif "calm" in tone_description:
        return f"🌟 {message}... 🌟"
    elif "energetic" in tone_description:
        return f"🚀 {message}!!! 🚀"
    elif "thoughtful" in tone_description:
        return f"📜 {message}... 📜"
    else:
        return message

def adam_the_woo_memorial():
    """
    Display a memorial message for Adam the Woo with simulated vocal tones.
    """
    voice_db = load_voice_database()
    
    messages = [
        "In loving memory of Adam the Woo. Your passion for Disney will always inspire us.",
        "Adam the Woo, you brought magic to our lives. Rest in peace.",
        "Remembering Adam the Woo, a true Disney legend. Your legacy lives on.",
        "Adam the Woo, your spirit and joy will forever be a part of the Disney community.",
        "In honor of Adam the Woo, may your love for Disney continue to shine brightly."
    ]
    
    print("\n" + "="*80)
    print("Adam the Woo Memorial Easter Egg")
    print("="*80 + "\n")
    
    for _ in range(5):
        message = random.choice(messages)
        tone = random.choice(voice_db["vocal_tones"])
        styled_message = simulate_vocal_tone(tone["description"], message)
        print(f"🌟 {styled_message} 🌟")
        time.sleep(2)
    
    print("\n" + "="*80)
    print("Adam the Woo, you will be deeply missed.")
    print("="*80 + "\n")

if __name__ == "__main__":
    adam_the_woo_memorial()


