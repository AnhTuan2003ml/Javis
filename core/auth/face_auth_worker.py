import json
import os
import sys
import time
from pathlib import Path

# Must be set before importing cv2 on Windows. Fixes many MSMF cannot-grab-frame cases.
os.environ.setdefault("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")
os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from core.auth.camera_utils import is_black_frame, open_preferred_camera_fast, open_working_camera

TRAINER_PATH = PROJECT_ROOT / "core" / "auth" / "trainer" / "trainer.yml"
CASCADE_PATH = PROJECT_ROOT / "core" / "auth" / "haarcascade_frontalface_default.xml"
RESULT_PATH = PROJECT_ROOT / "data" / "state" / "face_auth_result.json"


def write_result(success=False, user_id=None, message=""):
    try:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with RESULT_PATH.open("w", encoding="utf-8") as f:
            json.dump({"success": bool(success), "user_id": user_id, "message": message}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[FaceAuthWorker] Cannot write result: {e}", flush=True)


def main():
    write_result(False, None, "started")

    if not TRAINER_PATH.exists():
        print("Trainer file not found. Train first.", flush=True)
        write_result(False, None, "Trainer file not found")
        return 2

    if not CASCADE_PATH.exists():
        print("Cascade file missing.", flush=True)
        write_result(False, None, "Cascade file missing")
        return 2

    if not hasattr(cv2, "face"):
        print("cv2.face is missing. Install opencv-contrib-python.", flush=True)
        write_result(False, None, "cv2.face missing")
        return 2

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(TRAINER_PATH))
    face_cascade = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_cascade.empty():
        print("Cascade file cannot be loaded.", flush=True)
        write_result(False, None, "Cascade cannot load")
        return 2

    cam = None
    camera_info = None
    try:
        # First try the configured camera, but validate it can actually read frames.
        # If MSMF opens but cannot grab frames, fall back to full probing.
        try:
            cam, camera_info = open_preferred_camera_fast(validate=True)
        except Exception as e:
            print(f"[FaceAuthWorker] Preferred camera failed: {e}", flush=True)
            print("[FaceAuthWorker] Falling back to camera probing...", flush=True)
            cam, camera_info = open_working_camera(width=640, height=480, max_index=5, warmup_frames=6, allow_dark_fallback=False)

        print(f"[FaceAuthWorker] Camera selected: {camera_info}", flush=True)

        font = cv2.FONT_HERSHEY_SIMPLEX
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        match_count = 0
        required_matches = 3
        start_time = time.time()
        no_frame_count = 0

        while True:
            ret, frame = cam.read()
            if not ret or frame is None:
                no_frame_count += 1
                if no_frame_count % 30 == 0:
                    print("[FaceAuthWorker] Waiting for camera frame...", flush=True)
                if time.time() - start_time > 45:
                    print("[FaceAuthWorker] Timeout waiting for frame", flush=True)
                    write_result(False, None, "timeout waiting frame")
                    return 3
                time.sleep(0.03)
                continue

            no_frame_count = 0

            if is_black_frame(frame):
                cv2.putText(frame, "Black camera frame - check shutter/source", (10, 35), font, 0.65, (0, 0, 255), 2)
                cv2.imshow("JARVIS Face Auth", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    write_result(False, None, "user cancelled")
                    return 4
                if time.time() - start_time > 45:
                    print("[FaceAuthWorker] Timeout: camera frame stayed black", flush=True)
                    write_result(False, None, "black frame timeout")
                    return 3
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = float(np.mean(gray))
            if mean_brightness < 80:
                gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
            elif mean_brightness > 180:
                gray = cv2.convertScaleAbs(gray, alpha=0.7, beta=-20)
            gray = clahe.apply(gray)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)

            faces1 = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(60, 60))
            faces2 = face_cascade.detectMultiScale(gray, 1.05, 3, minSize=(50, 50))
            faces = []
            for (x, y, w, h) in list(faces1) + list(faces2):
                if w <= 50 or h <= 50:
                    continue
                duplicate = False
                for (ex, ey, ew, eh) in faces:
                    if abs(x - ex) < 30 and abs(y - ey) < 30:
                        duplicate = True
                        break
                if not duplicate:
                    faces.append((x, y, w, h))

            cv2.putText(frame, "Look at camera - ESC to cancel", (10, 25), font, 0.65, (255, 255, 255), 2)
            cv2.putText(frame, f"Faces: {len(faces)}", (10, 55), font, 0.55, (255, 255, 255), 1)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                predictions = []
                for size in (100, 150, 200):
                    resized_roi = cv2.resize(roi_gray, (size, size))
                    resized_roi = cv2.equalizeHist(resized_roi)
                    pred_id, conf = recognizer.predict(resized_roi)
                    predictions.append((pred_id, conf))

                pred_id, confidence = min(predictions, key=lambda item: item[1])
                accuracy = max(0, min(100, round(100 - confidence)))

                if confidence < 80:
                    match_count += 1
                    label = f"Verifying ID {pred_id}: {match_count}/{required_matches}"
                    color = (0, 255, 0)
                    if match_count >= required_matches:
                        print(f"JARVIS_AUTH_SUCCESS:{pred_id}", flush=True)
                        write_result(True, int(pred_id), "success")
                        return 0
                else:
                    match_count = max(match_count - 1, 0)
                    label = f"Unknown ID {pred_id} Conf {confidence:.1f}"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), font, 0.55, color, 2)
                cv2.putText(frame, f"Acc {accuracy}%", (x, y + h + 20), font, 0.55, (255, 255, 0), 1)

            cv2.imshow("JARVIS Face Auth", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                write_result(False, None, "user cancelled")
                return 4

            if time.time() - start_time > 45:
                print("[FaceAuthWorker] Face authentication timeout", flush=True)
                write_result(False, None, "face auth timeout")
                return 3

    except Exception as e:
        print(f"[FaceAuthWorker] Error: {e}", flush=True)
        write_result(False, None, str(e))
        return 1
    finally:
        try:
            if cam is not None:
                cam.release()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
