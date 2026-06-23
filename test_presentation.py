#!/usr/bin/env python3
"""Test AI Presentation Maker"""

from engine.dual_ai import DualAI

def test_presentation():
    # Initialize dual AI
    ai = DualAI()
    
    print("Testing AI Presentation Maker...")
    print("=" * 50)
    
    # Test 1: Text outline only
    print("\n1. Creating text outline:")
    result1 = ai._ai_presentation("Python Programming")
    print(result1)
    
    print("\n" + "=" * 50)
    
    # Test 2: Create PowerPoint file
    print("\n2. Creating PowerPoint file:")
    result2 = ai._ai_presentation("Artificial Intelligence", create_ppt=True)
    print(result2)
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_presentation()