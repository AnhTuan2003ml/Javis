# SIMPLE TRAINER - samples saved by sample.py are already cropped face images.

import os
import cv2
import numpy as np
from PIL import Image


def train_face_model():
    path = "core/auth/samples"
    out_dir = "core/auth/trainer"
    out_file = os.path.join(out_dir, "trainer.yml")

    if not os.path.exists(path):
        print("Error: Samples directory not found!")
        print("Run: python .\\core\\auth\\sample.py")
        return False

    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not image_paths:
        print("Error: No face samples found!")
        print("Run: python .\\core\\auth\\sample.py")
        return False

    if not hasattr(cv2, "face"):
        print("Error: cv2.face missing. Install opencv-contrib-python, not opencv-python only.")
        print("Command: python -m pip install --force-reinstall numpy==1.26.4 opencv-contrib-python==4.8.1.78")
        return False

    faces = []
    ids = []
    print(f"Found {len(image_paths)} sample images")

    for i, image_path in enumerate(image_paths, start=1):
        try:
            filename = os.path.basename(image_path)
            # Format: face.ID.count.jpg
            face_id = int(filename.split(".")[1])
            img = Image.open(image_path).convert("L")
            arr = np.array(img, "uint8")
            arr = cv2.resize(arr, (200, 200))
            faces.append(arr)
            ids.append(face_id)
            if i % 20 == 0:
                print(f"Loaded {i}/{len(image_paths)}")
        except Exception as e:
            print(f"Skip {image_path}: {e}")

    if not faces:
        print("Error: No valid samples to train")
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print(f"Training with {len(faces)} samples, IDs={sorted(set(ids))}")
    recognizer.train(faces, np.array(ids))

    os.makedirs(out_dir, exist_ok=True)
    recognizer.write(out_file)
    print(f"Training completed: {out_file}")
    return True


if __name__ == "__main__":
    train_face_model()
