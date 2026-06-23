import cv2
import os

try:
    # Create samples directory if it doesn't exist
    os.makedirs('engine\\auth\\samples', exist_ok=True)
    
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    
    detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')
    
    print("=== Jarvis Face Training ===")
    print("Instructions:")
    print("1. FRONT: Look directly at camera (62 photos)")
    print("2. LEFT: Turn head left (62 photos)")
    print("3. RIGHT: Turn head right (62 photos)")
    print("4. UP/DOWN: Tilt head up/down (64 photos)")
    print("5. Press ESC to stop early")
    print("6. 250 samples total from 4 angles")
    print()
    
    import json
    
    # Load existing users
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    name = input("Enter your name: ")
    
    # Auto-assign next available ID
    if users:
        face_id = str(max(int(k) for k in users.keys()) + 1)
    else:
        face_id = "1"
    
    # Save user to database
    users[face_id] = name
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"Assigned ID {face_id} to {name}")
    
    print(f"Starting face capture for {name} (ID: {face_id})...")
    print("Position your face in the camera frame...")
    
    count = 0
    total_photos = 250
    angles = ["FRONT", "LEFT", "RIGHT", "UP/DOWN"]
    photos_per_angle = [62, 62, 62, 64]
    current_angle = 0
    angle_count = 0
    
    while True:
        ret, img = cam.read()
        if not ret:
            print("Error: Could not read from camera")
            break
            
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply histogram equalization for better detection
        converted_image = cv2.equalizeHist(converted_image)
        
        faces = detector.detectMultiScale(
            converted_image, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            count += 1
            angle_count += 1
            
            # Save face sample with better quality
            face_sample = converted_image[y:y+h, x:x+w]
            face_sample = cv2.resize(face_sample, (200, 200))  # Consistent size
            
            cv2.imwrite(f"engine\\auth\\samples\\face.{face_id}.{count}.jpg", face_sample)
            
            # Check if need to switch angle
            if angle_count >= photos_per_angle[current_angle] and current_angle < 3:
                current_angle += 1
                angle_count = 0
                print(f"\nSwitch to: {angles[current_angle]}")
                cv2.waitKey(2000)  # 2 second pause
            
            # Show progress
            cv2.putText(img, f"Angle: {angles[current_angle]}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(img, f"Photos: {count}/{total_photos}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(img, "Press ESC to stop", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Jarvis Face Training - Look at Camera', img)
        
        k = cv2.waitKey(100) & 0xff
        if k == 27:  # ESC key
            break
        elif count >= total_photos:
            break
    
    print(f"\nCapture completed! {count} samples saved.")
    print("Now run 'py engine/auth/trainer.py' to train the model.")
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure your camera is working and not used by other applications.")
    
finally:
    try:
        cam.release()
        cv2.destroyAllWindows()
    except:
        pass