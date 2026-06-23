# FACE SAMPLE CAPTURE - supports IP camera.
# Default IP camera: http://192.168.1.5:8080

import os
os.environ.setdefault("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")

import json
import time
import cv2
import numpy as np


def load_camera_config():
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
        print(f"[Camera] config read failed: {e}")

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


def backend_value(name):
    name = str(name or "MSMF").upper()
    if name == "DSHOW":
        return cv2.CAP_DSHOW
    if name == "ANY":
        return cv2.CAP_ANY
    return cv2.CAP_MSMF


def show_message(window_name, message):
    img = np.zeros((360, 760, 3), dtype=np.uint8)
    y = 70
    for line in str(message).split("\n"):
        cv2.putText(img, line[:85], (25, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 1)
        y += 38
    cv2.imshow(window_name, img)


def open_camera_source(cfg):
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
    backend = backend_value(backend_name)
    print(f"[Camera] LOCAL: index={index}, backend={backend_name}")
    cap = cv2.VideoCapture(index, backend)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return {"mode": "cap", "cap": cap, "label": f"index={index} backend={backend_name}"}


def read_frame(source):
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


def release_camera_source(source):
    try:
        cap = source.get("cap")
        if cap is not None:
            cap.release()
    except Exception:
        pass


def main():
    os.makedirs("core/auth/samples", exist_ok=True)
    os.makedirs("data/state", exist_ok=True)

    cfg = load_camera_config()
    window_name = "Jarvis Face Training - IP Camera"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    show_message(window_name, "Opening camera source...\n" + str(cfg.get("source_type")))
    cv2.waitKey(300)

    source = open_camera_source(cfg)
    show_message(window_name, "Camera source:\n" + source.get("label", "unknown") + "\nWaiting for frame...")
    cv2.waitKey(300)

    detector = cv2.CascadeClassifier("core/auth/haarcascade_frontalface_default.xml")
    if detector.empty():
        print("Error: cascade file missing or invalid")
        show_message(window_name, "Cascade file missing/invalid\ncore/auth/haarcascade_frontalface_default.xml")
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        return

    try:
        with open("data/state/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = {}

    name = input("Enter your name: ").strip() or "user"
    face_id = str(max([int(k) for k in users.keys()] or [0]) + 1)
    users[face_id] = name
    with open("data/state/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print(f"Assigned ID {face_id} to {name}")
    print("Look at IP camera. Press ESC to stop.")

    count = 0
    total_photos = 120
    no_frame_count = 0
    last_save = 0

    while count < total_photos:
        ret, frame = read_frame(source)
        if not ret or frame is None:
            no_frame_count += 1
            show_message(window_name, "No frame from IP camera\nCheck phone IP camera app\n" + source.get("label", "") + f"\nfailed={no_frame_count}")
            print(f"[Camera] no frame #{no_frame_count}")
            if cv2.waitKey(300) & 0xFF == 27:
                break
            if no_frame_count >= 80:
                print("Too many failed reads. Stop.")
                break
            continue

        no_frame_count = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        cv2.putText(frame, f"ID:{face_id} {name} | Photos: {count}/{total_photos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, f"IP Camera: {source.get('label','')[:55]}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 255), 1)
        cv2.putText(frame, "ESC stop", (10, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 255), 1)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if time.time() - last_save > 0.08:
                face_sample = gray[y:y+h, x:x+w]
                face_sample = cv2.resize(face_sample, (200, 200))
                count += 1
                last_save = time.time()
                cv2.imwrite(f"core/auth/samples/face.{face_id}.{count}.jpg", face_sample)
                print(f"Saved sample {count}/{total_photos}")

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    release_camera_source(source)
    cv2.destroyAllWindows()
    print(f"Capture completed: {count} samples saved.")
    print("Next: python .\\core\\auth\\trainer.py")


if __name__ == "__main__":
    main()
