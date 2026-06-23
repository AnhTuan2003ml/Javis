#!/usr/bin/env python3
"""
Direct Phone Link Integration for Gemini Live
"""

import subprocess
import time
import os

def setup_phone_link_direct():
    print("📱 Phone Link Direct Setup")
    print("=" * 25)
    
    print("🚀 Step 1: Open Phone Link App")
    try:
        # Try to open Phone Link app directly
        subprocess.run("start ms-yourphone:", shell=True)
        print("✅ Phone Link app opened")
    except:
        print("⚠️ Opening Phone Link manually...")
        print("Press Win key and search 'Phone Link'")
    
    print("\n📱 Step 2: On Your Phone")
    print("1. Install 'Link to Windows' from Play Store")
    print("2. Open the app")
    print("3. Sign in with your Microsoft account")
    print("4. Follow the pairing process")
    
    print("\n🔧 Step 3: Enable Camera Access")
    print("1. In Phone Link app on PC:")
    print("   - Click Settings (gear icon)")
    print("   - Find 'Features' or 'Permissions'")
    print("   - Enable 'Camera' access")
    print("2. On your phone:")
    print("   - Allow camera permission when prompted")
    
    print("\n⏳ Step 4: Wait for Camera Setup")
    print("Phone Link will install virtual camera drivers...")
    
    input("\nPress Enter after completing Phone Link setup...")
    
    # Check for new cameras
    print("\n🔍 Checking for Phone Link camera...")
    import cv2
    
    cameras_found = []
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    cameras_found.append((i, w, h))
                cap.release()
        except:
            continue
    
    print(f"\n📹 Cameras detected: {len(cameras_found)}")
    for i, w, h in cameras_found:
        if w > 1280 or h > 720:
            print(f"📱 Camera {i}: {w}x{h} (Likely Phone Camera)")
        else:
            print(f"💻 Camera {i}: {w}x{h} (PC Camera)")
    
    if len(cameras_found) > 1:
        print("\n✅ Multiple cameras detected!")
        print("🚀 Starting Gemini Live with phone camera...")
        
        # Start Gemini Live
        subprocess.run("python gemini_live_test.py", shell=True)
    else:
        print("\n⚠️ Only PC camera detected")
        print("📋 Troubleshooting:")
        print("1. Make sure Phone Link pairing is complete")
        print("2. Check camera permissions in Phone Link settings")
        print("3. Restart Phone Link app")
        print("4. Try disconnecting and reconnecting phone")

def quick_phone_link_check():
    print("🔍 Quick Phone Link Status Check")
    print("=" * 30)
    
    # Check if Phone Link process is running
    try:
        result = subprocess.run('tasklist /FI "IMAGENAME eq YourPhone.exe"', 
                              shell=True, capture_output=True, text=True)
        if "YourPhone.exe" in result.stdout:
            print("✅ Phone Link app is running")
        else:
            print("❌ Phone Link app not running")
            print("💡 Start Phone Link app first")
    except:
        print("⚠️ Could not check Phone Link status")
    
    # Check cameras
    import cv2
    print("\n📹 Available Cameras:")
    
    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    if w > 1280:
                        print(f"📱 Camera {i}: {w}x{h} ← Phone Camera!")
                    else:
                        print(f"💻 Camera {i}: {w}x{h}")
                cap.release()
            else:
                print(f"❌ Camera {i}: Not available")
        except:
            continue

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Full Phone Link Setup")
    print("2. Quick Status Check")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        setup_phone_link_direct()
    else:
        quick_phone_link_check()
        
    print("\n🚀 After setup, run: python gemini_live_test.py")
    print("System will automatically use the best camera available!")