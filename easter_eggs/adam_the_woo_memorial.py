#!/usr/bin/env python3

"""
Adam the Woo Memorial Easter Egg
This script is a tribute to Adam the Woo, a beloved figure in the Disney community.
"""

import random
import time

def adam_the_woo_memorial():
    """
    Display a memorial message for Adam the Woo.
    """
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
        print(f"🌟 {message} 🌟")
        time.sleep(2)
    
    print("\n" + "="*80)
    print("Adam the Woo, you will be deeply missed.")
    print("="*80 + "\n")

if __name__ == "__main__":
    adam_the_woo_memorial()

