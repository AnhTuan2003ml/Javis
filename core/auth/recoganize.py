# FACE AUTH - supports IP camera.
# Default IP camera: http://192.168.1.5:8080

import os
os.environ.setdefault("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")

import json
import time
import cv2
import numpy as np


def _load_camera_config():
    cfg = {
        "source_type": "ip_snapshot",
        "ip_camera_url": "http://192.168.1.5:8080/video",
        "ip_snapshot_url": "http://192.168.1.5:8080/shot.jpg",
        "camera_index": 0,
        "camera_backend": "MSMF",
        "width": 640,
        "height": 480,
        "timeout_seconds": 30,
    }
    try:
        if os.path.exists("config/camera_config.json"):
            with open("config/camera_config.json", "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
    except Exception as e:
        print(f"[Camera] Could not read config/camera_config.json: {e}")

    if os.environ.get("JARVIS_CAMERA_SOURCE"):
        cfg["source_type"] = os.environ["JARVIS_CAMERA_SOURCE"].strip().lower()
    if os.environ.get("JARVIS_IP_CAMERA_URL"):
        cfg["ip_camera_url"] = os.environ["JARVIS_IP_CAMERA_URL"].strip()
    if os.environ.get("JARVIS_IP_SNAPSHOT_URL"):
        cfg["ip_snapshot_url"] = os.environ["JARVIS_IP_SNAPSHOT_URL"].strip()
    if os.environ.get("JARVIS_CAMERA_INDEX") is not None:
        try:
            cfg["camera_index"] = int(os.environ["JARVIS_CAMERA_INDEX"])
        except ValueError:
            pass
    if os.environ.get("JARVIS_CAMERA_BACKEND"):
        cfg["camera_backend"] = os.environ["JARVIS_CAMERA_BACKEND"].upper()
    return cfg


def _backend_value(name):
    name = str(name or "MSMF").upper()
    if name == "DSHOW":
        return cv2.CAP_DSHOW
    if name == "ANY":
        return cv2.CAP_ANY
    return cv2.CAP_MSMF


def _show_message(window_name, message, seconds=3):
    img = np.zeros((360, 760, 3), dtype=np.uint8)
    y = 70
    for line in str(message).split("\n"):
        cv2.putText(img, line[:85], (25, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 1)
        y += 38
    cv2.imshow(window_name, img)
    end = time.time() + seconds
    while time.time() < end:
        if cv2.waitKey(100) & 0xFF == 27:
            break


def _open_camera_source(cfg):
    source_type = str(cfg.get("source_type", "ip_snapshot")).lower()
    width = int(cfg.get("width", 640))
    height = int(cfg.get("height", 480))

    if source_type in ("ip", "ip_stream", "ip_camera", "stream"):
        url = cfg.get("ip_camera_url") or "http://192.168.1.5:8080/video"
        print(f"[Camera] IP STREAM: {url}")
        cap = cv2.VideoCapture(url)
        return {"mode": "cap", "cap": cap, "label": url}

    if source_type in ("ip_snapshot", "snapshot", "http_snapshot"):
        url = cfg.get("ip_snapshot_url") or "http://192.168.1.5:8080/shot.jpg"
        print(f"[Camera] IP SNAPSHOT: {url}")
        return {"mode": "snapshot", "url": url, "label": url}

    index = int(cfg.get("camera_index", 0))
    backend_name = str(cfg.get("camera_backend", "MSMF")).upper()
    backend = _backend_value(backend_name)
    print(f"[Camera] LOCAL: index={index}, backend={backend_name}")
    cap = cv2.VideoCapture(index, backend)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return {"mode": "cap", "cap": cap, "label": f"index={index} backend={backend_name}"}


def _read_frame(source):
    if source.get("mode") == "snapshot":
        try:
            import requests
            resp = requests.get(source["url"], timeout=3)
            resp.raise_for_status()
            arr = np.frombuffer(resp.content, dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                return False, None
            return True, frame
        except Exception as e:
            print(f"[Camera] snapshot read failed: {e}")
            return False, None

    cap = source.get("cap")
    if cap is None or not cap.isOpened():
        return False, None
    return cap.read()


def _release_camera_source(source):
    try:
        cap = source.get("cap")
        if cap is not None:
            cap.release()
    except Exception:
        pass


def AuthenticateFace():
    window_name = "JARVIS Face Auth - IP Camera"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    _show_message(window_name, "Opening IP camera...", seconds=1)

    trainer_path = "core/auth/trainer/trainer.yml"
    cascade_path = "core/auth/haarcascade_frontalface_default.xml"

    if not os.path.exists(trainer_path):
        print("Trainer file not found. Train first.")
        _show_message(window_name, "Trainer file not found.\nRun: python .\\core\\auth\\sample.py\nThen: python .\\core\\auth\\trainer.py", seconds=5)
        cv2.destroyWindow(window_name)
        return 0, None

    if not os.path.exists(cascade_path):
        print("Cascade file missing.")
        _show_message(window_name, "Cascade file missing:\ncore/auth/haarcascade_frontalface_default.xml", seconds=5)
        cv2.destroyWindow(window_name)
        return 0, None

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_path)
    except Exception as e:
        print(f"Could not load face recognizer: {e}")
        _show_message(window_name, f"Could not load trainer/model.\n{e}", seconds=5)
        cv2.destroyWindow(window_name)
        return 0, None

    cfg = _load_camera_config()
    source = _open_camera_source(cfg)
    _show_message(window_name, "Camera source:\n" + source.get("label", "unknown") + "\nWaiting for frame...", seconds=1)

    face_cascade = cv2.CascadeClassifier(cascade_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    required_matches = 3
    match_count = 0
    start_time = time.time()
    timeout = int(cfg.get("timeout_seconds", 30))
    no_frame_count = 0

    while True:
        ret, frame = _read_frame(source)

        if not ret or frame is None:
            no_frame_count += 1
            msg = np.zeros((360, 760, 3), dtype=np.uint8)
            cv2.putText(msg, "No frame from IP camera", (25, 95), font, 0.75, (255, 255, 255), 2)
            cv2.putText(msg, source.get("label", "")[:80], (25, 145), font, 0.50, (255, 255, 255), 1)
            cv2.putText(msg, "Check phone IP camera app / WiFi", (25, 195), font, 0.60, (255, 255, 255), 1)
            cv2.putText(msg, "Press ESC to skip", (25, 245), font, 0.60, (255, 255, 255), 1)
            cv2.imshow(window_name, msg)
            print(f"[Camera] no frame #{no_frame_count}")
            if cv2.waitKey(300) & 0xFF == 27:
                break
            if no_frame_count >= 80:
                print("[Camera] Too many failed frames, stop Face Auth.")
                break
            continue

        no_frame_count = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

        cv2.putText(frame, "IP FACE AUTH - Press ESC to skip", (10, 28), font, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, source.get("label", "")[:65], (10, 58), font, 0.48, (0, 255, 255), 1)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            try:
                id_pred, confidence = recognizer.predict(roi)
            except Exception:
                id_pred, confidence = -1, 999

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{id_pred} Conf:{confidence:.1f}", (x, y+h+25), font, 0.55, (0, 255, 255), 1)

            if confidence < 85:
                match_count += 1
                cv2.putText(frame, f"Verifying {match_count}/{required_matches}", (10, 90), font, 0.65, (0, 255, 0), 2)
                if match_count >= required_matches:
                    print(f"Authenticated: User ID {id_pred}")
                    _release_camera_source(source)
                    cv2.destroyAllWindows()
                    return 1, id_pred
            else:
                match_count = max(match_count - 1, 0)

        cv2.imshow(window_name, frame)

        if time.time() - start_time > timeout:
            print("Face Auth timeout")
            break
        if cv2.waitKey(1) & 0xFF == 27:
            print("Face Auth skipped by ESC")
            break

    _release_camera_source(source)
    cv2.destroyAllWindows()
    return 0, None


if __name__ == "__main__":
    print(AuthenticateFace())
