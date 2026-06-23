import cv2
import numpy as np
from PIL import Image
import os

def train_face_model():
    path = 'engine\\auth\\samples'
    
    # Check if samples directory exists
    if not os.path.exists(path):
        print("Error: Samples directory not found!")
        print("Please run 'py engine/auth/sample.py' first to capture face samples.")
        return False
    
    # Check if there are sample images
    sample_files = [f for f in os.listdir(path) if f.endswith('.jpg')]
    if not sample_files:
        print("Error: No face samples found!")
        print("Please run 'py engine/auth/sample.py' first to capture face samples.")
        return False
    
    print(f"Found {len(sample_files)} face samples")
    
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
        
        def Images_And_Labels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
            faceSamples = []
            ids = []
            
            print("Processing face samples...")
            
            for i, imagePath in enumerate(imagePaths):
                try:
                    # Show progress
                    if i % 10 == 0:
                        print(f"Processing image {i+1}/{len(imagePaths)}")
                    
                    gray_img = Image.open(imagePath).convert('L')
                    img_arr = np.array(gray_img, 'uint8')
                    
                    # Extract ID from filename (face.ID.count.jpg)
                    filename = os.path.split(imagePath)[-1]
                    id = int(filename.split(".")[1])
                    
                    # Detect faces in the image
                    faces = detector.detectMultiScale(img_arr, scaleFactor=1.1, minNeighbors=5)
                    
                    for (x, y, w, h) in faces:
                        face_sample = img_arr[y:y+h, x:x+w]
                        # Resize for consistency
                        face_sample = cv2.resize(face_sample, (100, 100))
                        faceSamples.append(face_sample)
                        ids.append(id)
                        
                except Exception as e:
                    print(f"Error processing {imagePath}: {e}")
                    continue
            
            return faceSamples, ids
        
        print("=== Jarvis Face Model Training ===")
        print("Training faces. This may take a few moments...")
        
        faces, ids = Images_And_Labels(path)
        
        if not faces:
            print("Error: No valid face samples found for training!")
            return False
        
        print(f"Training with {len(faces)} face samples...")
        
        # Train the recognizer
        recognizer.train(faces, np.array(ids))
        
        # Create trainer directory if it doesn't exist
        os.makedirs('engine\\auth\\trainer', exist_ok=True)
        
        # Save the trained model
        recognizer.write('engine\\auth\\trainer\\trainer.yml')
        
        print("\n✅ Training completed successfully!")
        print("Face recognition model saved as trainer.yml")
        print("You can now use Jarvis face authentication.")
        
        return True
        
    except Exception as e:
        print(f"Training failed: {e}")
        print("Make sure OpenCV is properly installed with face recognition support.")
        return False

if __name__ == "__main__":
    train_face_model()