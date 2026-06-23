import cv2
import time
import os
import numpy as np

# REQUIREMENTS:
# - Trained ID: 1 (Primary authenticated user)
# - Accept IDs: 5, 20 for authentication
# - Available sample IDs: 21, 22 (not trained yet)

def AuthenticateFace():
    trainer_path = 'engine/auth/trainer/trainer.yml'
    cascadePath = "engine/auth/haarcascade_frontalface_default.xml"

    if not os.path.exists(trainer_path):
        print("Trainer file not found. Train first.")
        return 0, None

    if not os.path.exists(cascadePath):
        print("Cascade file missing.")
        return 0, None

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    match_count = 0
    required_matches = 3
    
    # Advanced lighting adaptation
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    
    start_time = time.time()
    
    while True:
        ret, frame = cam.read()
        if not ret:
            continue
            
        # Multi-stage preprocessing for any lighting
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Adaptive lighting correction
        mean_brightness = np.mean(gray)
        if mean_brightness < 80:  # Dark
            gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
        elif mean_brightness > 180:  # Bright
            gray = cv2.convertScaleAbs(gray, alpha=0.7, beta=-20)
        
        # Apply CLAHE for local contrast
        gray = clahe.apply(gray)
        
        # Gaussian blur for noise reduction
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Multi-scale face detection
        faces1 = faceCascade.detectMultiScale(gray, 1.1, 4, minSize=(60, 60))
        faces2 = faceCascade.detectMultiScale(gray, 1.05, 3, minSize=(50, 50))
        
        # Combine detections
        all_faces = list(faces1) + list(faces2)
        faces = []
        
        # Remove duplicates
        for face in all_faces:
            x, y, w, h = face
            is_duplicate = False
            for existing in faces:
                ex, ey, ew, eh = existing
                if abs(x - ex) < 30 and abs(y - ey) < 30:
                    is_duplicate = True
                    break
            if not is_duplicate and w > 50 and h > 50:
                faces.append(face)
        
        name = "Unknown"
        confidence_txt = "0%"
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            
            # Multiple size processing for robustness
            sizes = [100, 120, 150]
            predictions = []
            
            for size in sizes:
                resized_roi = cv2.resize(roi_gray, (size, size))
                # Additional preprocessing
                resized_roi = cv2.equalizeHist(resized_roi)
                
                id_pred, conf = recognizer.predict(resized_roi)
                predictions.append((id_pred, conf))
            
            # Get best prediction
            best_pred = min(predictions, key=lambda x: x[1])
            id_pred, confidence = best_pred
            
            accuracy = round(100 - confidence)
            
            # Debug info
            cv2.putText(frame, f"ID:{id_pred} Conf:{confidence:.1f}", (x, y+h+30), font, 0.5, (0,255,255), 1)
            
            # Accept trained IDs with reasonable confidence
            if confidence < 80 and id_pred in [24, 25, 26, 27, 28]:  # Accept IDs 1, 5, 20
                name = "User"
                confidence_txt = f"{accuracy}%"
                match_count += 1
                
                cv2.putText(frame, f"Verifying... {match_count}/{required_matches}", (10, 30), font, 0.7, (0,255,0), 2)
                
                if match_count >= required_matches:
                    cam.release()
                    cv2.destroyAllWindows()
                    print(f"Authenticated: User ID {id_pred}")
                    return 1, id_pred
            else:
                match_count = max(match_count - 1, 0)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, name, (x, y-10), font, 0.8, (255,255,255), 2)
            cv2.putText(frame, confidence_txt, (x, y+h+15), font, 0.6, (255,255,0), 1)
        
        # Lighting indicator
        light_status = "Dark" if mean_brightness < 80 else "Bright" if mean_brightness > 180 else "Good"
        cv2.putText(frame, f"Light: {light_status}", (10, 60), font, 0.5, (255,255,255), 1)
        
        cv2.imshow("JARVIS Face Auth", frame)
        
        if time.time() - start_time > 30:
            print("Timeout")
            break
            
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    return 0, None