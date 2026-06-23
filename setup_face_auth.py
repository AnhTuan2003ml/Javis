#!/usr/bin/env python3
"""
JARVIS Enhanced Face Authentication Setup
Complete setup and configuration for face authentication system
"""

import os
import sys
import subprocess
import json

def check_dependencies():
    """Check if required packages are installed"""
    print("=== Checking Dependencies ===")
    
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'PIL': 'Pillow'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - Missing")
            missing_packages.append(package)
    
    # Check for opencv-contrib-python (needed for face recognition)
    try:
        import cv2
        cv2.face.LBPHFaceRecognizer_create()
        print("✓ opencv-contrib-python (face recognition)")
    except AttributeError:
        print("✗ opencv-contrib-python - Missing or incomplete")
        missing_packages.append('opencv-contrib-python')
    except ImportError:
        pass  # Already handled above
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✓ All dependencies satisfied!")
    return True

def setup_directories():
    """Create necessary directories"""
    print("\n=== Setting Up Directories ===")
    
    directories = [
        'engine\\auth\\samples',
        'engine\\auth\\trainer'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ {directory}")
        except Exception as e:
            print(f"✗ {directory}: {e}")
            return False
    
    return True

def check_cascade_file():
    """Check if Haar cascade file exists"""
    print("\n=== Checking Cascade File ===")
    
    cascade_path = "engine\\auth\\haarcascade_frontalface_default.xml"
    
    if os.path.exists(cascade_path):
        print("✓ Haar cascade file found")
        return True
    
    print("✗ Haar cascade file missing")
    print("Downloading from OpenCV repository...")
    
    try:
        import urllib.request
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(url, cascade_path)
        print("✓ Cascade file downloaded")
        return True
    except Exception as e:
        print(f"✗ Failed to download: {e}")
        print("Please download manually from:")
        print("https://github.com/opencv/opencv/tree/master/data/haarcascades")
        return False

def test_camera():
    """Test camera functionality"""
    print("\n=== Testing Camera ===")
    
    try:
        import cv2
        
        # Try different camera indices and backends
        for camera_index in [0, 1, 2]:
            for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
                try:
                    cam = cv2.VideoCapture(camera_index, backend)
                    if cam.isOpened():
                        ret, frame = cam.read()
                        if ret and frame is not None:
                            print(f"✓ Camera {camera_index} working")
                            cam.release()
                            return True
                        cam.release()
                except:
                    continue
        
        print("✗ No working camera found")
        return False
        
    except ImportError:
        print("✗ OpenCV not available")
        return False

def create_config_files():
    """Create initial configuration files"""
    print("\n=== Creating Configuration ===")
    
    # Create users.json if it doesn't exist
    users_file = 'users.json'
    if not os.path.exists(users_file):
        try:
            with open(users_file, 'w') as f:
                json.dump({}, f, indent=2)
            print("✓ users.json created")
        except Exception as e:
            print(f"✗ Failed to create users.json: {e}")
            return False
    else:
        print("✓ users.json exists")
    
    return True

def run_setup_wizard():
    """Interactive setup wizard"""
    print("JARVIS Enhanced Face Authentication Setup")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        print("Please install required packages and run setup again.")
        return False
    
    # Step 2: Setup directories
    if not setup_directories():
        print("\n❌ Setup failed: Could not create directories")
        return False
    
    # Step 3: Check cascade file
    if not check_cascade_file():
        print("\n❌ Setup failed: Cascade file missing")
        return False
    
    # Step 4: Test camera
    if not test_camera():
        print("\n⚠️  Warning: No camera detected")
        print("Face authentication requires a working camera.")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    # Step 5: Create config files
    if not create_config_files():
        print("\n❌ Setup failed: Could not create configuration")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run 'py engine/auth/test_camera.py' to test your setup")
    print("2. Run 'py engine/auth/sample.py' to register your face")
    print("3. Run 'py engine/auth/trainer.py' to train the model")
    print("4. Use face authentication in your JARVIS system")
    
    return True

def quick_test():
    """Run a quick system test"""
    print("\n=== Quick System Test ===")
    
    try:
        # Import test module
        sys.path.append('engine\\auth')
        from test_camera import run_full_test
        
        print("Running comprehensive test...")
        return run_full_test()
        
    except ImportError:
        print("Test module not found, running basic checks...")
        
        # Basic checks
        checks = [
            check_dependencies(),
            os.path.exists('engine\\auth\\haarcascade_frontalface_default.xml'),
            test_camera()
        ]
        
        return all(checks)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
    else:
        run_setup_wizard()