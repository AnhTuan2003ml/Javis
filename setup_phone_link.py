#!/usr/bin/env python3
"""
Phone Link Camera Setup - Step by Step
"""

def check_phone_link_status():
    print("📱 Phone Link Camera Setup")
    print("=" * 30)
    
    # Check if Phone Link is installed
    import subprocess
    import os
    
    print("🔍 Checking Phone Link installation...")
    
    # Check if Phone Link app exists
    phone_link_paths = [
        "C:\\Program Files\\WindowsApps\\Microsoft.YourPhone*",
        "C:\\Users\\%USERNAME%\\AppData\\Local\\Packages\\Microsoft.YourPhone*"
    ]
    
    phone_link_found = False
    for path in phone_link_paths:
        if os.path.exists(path.replace("*", "")):
            phone_link_found = True
            break
    
    if phone_link_found:
        print("✅ Phone Link app detected")
    else:
        print("❌ Phone Link not found")
        print("📥 Install from Microsoft Store: ms-windows-store://pdp/?productid=9NMPJ99VJBWV")
    
    # Check available cameras
    print("\n🔍 Checking all cameras...")
    import cv2
    
    cameras = []
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    cameras.append((i, w, h))
                    print(f"✅ Camera {i}: {w}x{h}")
                cap.release()
            else:
                print(f"❌ Camera {i}: Not available")
        except:
            print(f"❌ Camera {i}: Error")
    
    # Analyze cameras
    if len(cameras) == 1:
        print(f"\n⚠️ Only 1 camera found (Camera {cameras[0][0]})")
        print("📱 Phone Link camera not detected")
        print("\n🔧 Setup Steps:")
        print("1. Open Phone Link app on PC")
        print("2. Install 'Link to Windows' on your phone")
        print("3. Pair your devices")
        print("4. In Phone Link settings, enable 'Camera' permission")
        print("5. Restart this script to check again")
    elif len(cameras) > 1:
        print(f"\n✅ Multiple cameras found!")
        for i, w, h in cameras:
            if w > 1280 or h > 720:
                print(f"📱 Camera {i} might be phone camera: {w}x{h}")
            else:
                print(f"💻 Camera {i} is likely PC camera: {w}x{h}")
    else:
        print("\n❌ No cameras found!")
    
    print(f"\n🚀 To use phone camera in Gemini Live:")
    print("1. Complete Phone Link setup above")
    print("2. Run: python gemini_live_test.py")
    print("3. System will auto-select highest resolution camera")

def setup_phone_link_step_by_step():
    print("\n📋 Phone Link Setup Instructions:")
    print("=" * 35)
    
    print("\n🖥️ On Your PC:")
    print("1. Press Win + I to open Settings")
    print("2. Go to 'Bluetooth & devices' > 'Phone Link'")
    print("3. Click 'Set up a new device'")
    print("4. Choose 'Android'")
    
    print("\n📱 On Your Phone:")
    print("1. Install 'Link to Windows' from Play Store")
    print("2. Open the app and sign in with Microsoft account")
    print("3. Follow pairing instructions")
    
    print("\n🔧 Enable Camera Access:")
    print("1. In Phone Link app on PC, go to Settings")
    print("2. Find 'Camera' or 'Permissions' section")
    print("3. Enable camera access")
    print("4. Your phone camera will appear as virtual webcam")
    
    print("\n✅ Test Setup:")
    print("Run this script again to verify camera detection")

if __name__ == "__main__":
    check_phone_link_status()
    setup_phone_link_step_by_step()